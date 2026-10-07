from pathlib import Path

from pdf_parser import extract_transactions
from fifo import calculate_fifo


# Find the project folder
project_folder = Path(__file__).resolve().parent.parent

# Find the sample PDF
pdf_path = project_folder / "sample_contract_note_equity_project.pdf"


# Step 1: Read PDF
transactions = extract_transactions(pdf_path)

print("\nExtracted Transactions:")
print(transactions.to_string(index=False))


# Step 2: Send transactions to FIFO
realised_profit, remaining_lots, matches = calculate_fifo(transactions)


# Step 3: Display result
print("\n-------------------------")
print("FIFO RESULT")
print("-------------------------")

print("Realised Profit:", realised_profit)

print("\nRemaining Lots:")

for stock, lots in remaining_lots.items():

    print(stock)

    for lot in lots:
        print(
            "  Quantity:",
            lot["quantity"],
            "Price:",
            lot["price"]
        )