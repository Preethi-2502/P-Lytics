from pathlib import Path

from pdf_parser import (
    extract_transactions,
    extract_charges
)

from fifo import calculate_fifo

from database import (
    create_tables,
    clear_charge_records,
    insert_charge_records,
    get_charge_records
)

from charges import (
    apply_sell_charges_to_matches
)


# --------------------------------
# Find sample PDF
# --------------------------------

project_folder = Path(__file__).resolve().parent.parent

pdf_path = (
    project_folder /
    "sample_contract_note_equity_project.pdf"
)


# --------------------------------
# Create database tables
# --------------------------------

create_tables()


# --------------------------------
# Read transactions
# --------------------------------

transactions = extract_transactions(
    pdf_path
)


# --------------------------------
# Read charges from PDF
# --------------------------------

charges = extract_charges(
    pdf_path
)


# --------------------------------
# Store charges
# --------------------------------

clear_charge_records()

insert_charge_records(
    charges
)


# --------------------------------
# Read charges from database
# --------------------------------

charge_records = get_charge_records()


# --------------------------------
# Run FIFO
# --------------------------------

realised_profit, remaining_lots, matches = calculate_fifo(
    transactions
)


# --------------------------------
# Apply actual SELL charges
# --------------------------------

updated_matches = apply_sell_charges_to_matches(
    matches,
    charge_records
)


# --------------------------------
# Display
# --------------------------------

print("\nFIFO + ACTUAL CHARGES")
print("=" * 50)


total_net_profit = 0


for match in updated_matches:

    print(
        "\nStock:",
        match["Stock"]
    )

    print(
        "Quantity:",
        match["Quantity"]
    )

    print(
        "Buy Price:",
        match["Buy Price"]
    )

    print(
        "Sell Price:",
        match["Sell Price"]
    )

    print(
        "Gross P&L:",
        match["Gross P&L"]
    )

    print(
        "Allocated Charges:",
        match["Allocated Charges"]
    )

    print(
        "Net P&L:",
        match["Net P&L"]
    )

    total_net_profit += (
        match["Net P&L"]
    )


print("\n" + "=" * 50)

print(
    "Gross Realised P&L:",
    realised_profit
)

print(
    "Total SELL Charges:",
    sum(
        charge["Total Charges"]
        for charge in charge_records
        if charge["Type"].upper() == "SELL"
    )
)

print(
    "Net Realised P&L:",
    total_net_profit
)