from pathlib import Path

from pdf_parser import extract_transactions

from database import (
    create_tables,
    clear_transactions,
    insert_transactions,
    get_connection
)


# Project folder
project_folder = Path(__file__).resolve().parent.parent

# Sample PDF
pdf_path = project_folder / "sample_contract_note_equity_project.pdf"


# 1. Create tables
create_tables()

# 2. Clear old data
clear_transactions()

# 3. Extract PDF transactions
transactions = extract_transactions(pdf_path)

print("\nExtracted Transactions:")
print(transactions.to_string(index=False))


# 4. Insert into database
insert_transactions(transactions)

print("\nTransactions inserted successfully!")


# 5. Read from database
connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT id, trade_date, stock, trade_type, quantity, price
    FROM transactions
""")

rows = cursor.fetchall()

connection.close()


# 6. Display stored data
print("\nStored Transactions:")
print("--------------------------------")

for row in rows:
    print(row)