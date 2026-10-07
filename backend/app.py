from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from pathlib import Path

from pdf_parser import (
    extract_transactions,
    extract_charges
)

from database import (
    create_tables,
    clear_transactions,
    insert_transactions,
    get_all_transactions,
    get_charge_records,
    clear_charge_records,
    insert_charge_records,
    get_corporate_actions
)

from fifo import calculate_fifo

from pnl import calculate_unrealised_pnl

from charges import apply_sell_charges_to_matches

from portfolio_engine import (
    build_portfolio_events,
    process_events
)
# =================================
# CREATE FLASK APP
# =================================

app = Flask(__name__)
CORS(app)


# =================================
# UPLOAD FOLDER
# =================================

PROJECT_FOLDER = Path(__file__).resolve().parent.parent

UPLOAD_FOLDER = PROJECT_FOLDER / "uploads"

UPLOAD_FOLDER.mkdir(exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
def calculate_portfolio_result(current_prices):

    # =================================
    # GET DATABASE DATA
    # =================================

    transactions = get_all_transactions()

    corporate_actions = get_corporate_actions()

    charge_records = get_charge_records()


    # =================================
    # NO TRANSACTIONS
    # =================================

    if not transactions:

        return {
            "realised_profit": 0,
            "unrealised_profit": 0,
            "total_pnl": 0,
            "total_charges": 0,
            "holdings": [],
            "remaining_lots": {},
            "fifo_matches": []
        }


    # =================================
    # BUILD ALL EVENTS
    # =================================

    events = build_portfolio_events(
        transactions,
        corporate_actions
    )


    # =================================
    # PROCESS FIFO + BUY CHARGES
    # =================================

    realised_profit, remaining_lots, matches = (
        process_events(
            events,
            charge_records
        )
    )


    # =================================
    # APPLY SELL CHARGES
    # =================================

    if charge_records:

        updated_matches = (
            apply_sell_charges_to_matches(
                matches,
                charge_records
            )
        )

    else:

        updated_matches = []

        for match in matches:

            updated_match = match.copy()

            updated_match["Allocated Charges"] = 0

            updated_match["Net P&L"] = (
                match["Gross P&L"]
            )

            updated_matches.append(
                updated_match
            )


    # =================================
    # NET REALISED P&L
    # =================================

    net_realised_profit = sum(

        match["Net P&L"]

        for match in updated_matches

    )


    # =================================
    # TOTAL SELL CHARGES
    # =================================

    total_charges = sum(

        float(charge["Total Charges"])

        for charge in charge_records

        if charge["Type"].upper() == "SELL"

    )


    # =================================
    # UNREALISED P&L
    # =================================

    holdings, unrealised_profit = (
        calculate_unrealised_pnl(
            remaining_lots,
            current_prices
        )
    )


    # =================================
    # TOTAL P&L
    # =================================

    total_pnl = (
        net_realised_profit +
        unrealised_profit
    )


    # =================================
    # CONVERT LOTS FOR JSON
    # =================================

    remaining = {}

    for stock, lots in remaining_lots.items():

        remaining[stock] = list(lots)


    # =================================
    # FINAL RESULT
    # =================================

    return {

        "realised_profit":
            net_realised_profit,

        "unrealised_profit":
            unrealised_profit,

        "total_pnl":
            total_pnl,

        "total_charges":
            total_charges,

        "holdings":
            holdings,

        "remaining_lots":
            remaining,

        "fifo_matches":
            updated_matches

    }

# =================================
# CREATE DATABASE TABLES
# =================================

create_tables()
def calculate_net_realised_pnl(transactions):

    # Run FIFO
    realised_profit, remaining_lots, matches = calculate_fifo(
        transactions
    )

    # Get charges stored in database
    charge_records = get_charge_records()

    # Apply SELL charges to FIFO matches
    updated_matches = apply_sell_charges_to_matches(
        matches,
        charge_records
    )

    # Calculate net realised P&L
    if updated_matches:

        net_realised_profit = sum(
            match["Net P&L"]
            for match in updated_matches
        )

    else:

        net_realised_profit = realised_profit

    return (
        net_realised_profit,
        remaining_lots,
        matches,
        updated_matches
    )

# =================================
# HOME API
# =================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Portfolio P&L Calculator Backend is running!"
    })


# =================================
# UPLOAD CONTRACT NOTE
# =================================

@app.route("/upload", methods=["POST"])
def upload_file():

    # Check whether a file was uploaded
    if "file" not in request.files:

        return jsonify({
            "error": "No file uploaded"
        }), 400


    file = request.files["file"]


    # Check filename
    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400


    # Only PDF files are allowed
    if not file.filename.lower().endswith(".pdf"):

        return jsonify({
            "error": "Only PDF files are allowed"
        }), 400


    # Make filename safe
    filename = secure_filename(
        file.filename
    )


    # Create file path
    file_path = (
        UPLOAD_FOLDER / filename
    )


    # Save uploaded PDF
    file.save(file_path)


    try:

        # =================================
        # 1. EXTRACT TRANSACTIONS
        # =================================

        transactions = extract_transactions(
            file_path
        )


        # =================================
        # 2. EXTRACT CHARGES
        # =================================

        charges = extract_charges(
            file_path
        )


        # =================================
        # 3. CLEAR OLD DATA
        # =================================

        clear_transactions()

        clear_charge_records()


        # =================================
        # 4. STORE NEW DATA
        # =================================

        insert_transactions(
            transactions
        )

        insert_charge_records(
            charges
        )


        # =================================
        # 5. CALCULATE PORTFOLIO
        # =================================

        current_prices = {

            "ALPHA": 140,

            "BETA": 70,

            "GAMMA": 230

        }


        result = calculate_portfolio_result(
            current_prices
        )


        # =================================
        # 6. RETURN RESULT
        # =================================

        return jsonify({

            "message":
                "Contract note processed successfully",

            **result

        })


    except Exception as error:

        return jsonify({

            "error":
                str(error)

        }), 500

# =================================
# GET ALL TRANSACTIONS
# =================================

@app.route("/transactions", methods=["GET"])
def get_transactions():

    transactions = get_all_transactions()

    return jsonify({

        "transactions":
            transactions

    })


# =================================
# GET PORTFOLIO
# =================================

@app.route("/portfolio", methods=["GET"])
def get_portfolio():

    current_prices = {
        "ALPHA": 140,
        "BETA": 70,
        "GAMMA": 230
    }

    result = calculate_portfolio_result(
        current_prices
    )

    return jsonify(result)


# =================================
# UPDATE PORTFOLIO USING NEW PRICES
# =================================

@app.route("/portfolio", methods=["POST"])
def calculate_portfolio():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No JSON data received"
        }), 400


    current_prices = data.get(
        "current_prices",
        {}
    )


    result = calculate_portfolio_result(
        current_prices
    )


    return jsonify(result)


# =================================
# RUN FLASK
# =================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )