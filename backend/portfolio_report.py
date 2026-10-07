from pathlib import Path
from charges import calculate_net_pnl
from pdf_parser import extract_transactions
from fifo import calculate_fifo
from pnl import calculate_unrealised_pnl


def generate_report(pdf_path, current_prices):

    # 1. Extract transactions from PDF
    transactions = extract_transactions(pdf_path)

    # 2. Calculate realised P&L using FIFO
    realised_profit, remaining_lots, matches = calculate_fifo(transactions)

    # 3. Calculate unrealised P&L
    holdings, unrealised_profit = calculate_unrealised_pnl(
        remaining_lots,
        current_prices
    )

    # 4. Calculate total P&L
    total_pnl = realised_profit + unrealised_profit
    # Temporary total charges for prototype testing
    brokerage = 50
    stt = 30
    other_charges = 10

    total_charges, net_pnl = calculate_net_pnl(
        total_pnl,
        brokerage,
        stt,
        other_charges
    )

    return {
        "realised_profit": realised_profit,
        "unrealised_profit": unrealised_profit,
        "total_pnl": total_pnl,
        "total_charges": total_charges,
        "net_pnl": net_pnl,
        "holdings": holdings,
        "transactions": transactions
    }


if __name__ == "__main__":

    # Find project folder
    project_folder = Path(__file__).resolve().parent.parent

    # Sample contract note
    pdf_path = project_folder / "sample_contract_note_equity_project.pdf"

    # Current market prices
    current_prices = {
        "ALPHA": 140,
        "BETA": 70,
        "GAMMA": 230
    }

    report = generate_report(
        pdf_path,
        current_prices
    )

    print("\n==============================")
    print("PORTFOLIO P&L REPORT")
    print("==============================")

    print("Realised P&L   : ₹", report["realised_profit"])
    print("Unrealised P&L : ₹", report["unrealised_profit"])
    print("Total P&L      : ₹", report["total_pnl"])

    print("\nCurrent Holdings:")
    print(report["holdings"])
    print("Total Charges  : ₹", report["total_charges"])
    print("Net P&L        : ₹", report["net_pnl"])
