from pathlib import Path

from pdf_parser import extract_charges

from database import (
    create_tables,
    clear_charge_records,
    insert_charge_records,
    get_charge_records
)


# Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Sample PDF
pdf_path = project_folder / "sample_contract_note_equity_project.pdf"


# 1. Create tables
create_tables()


# 2. Remove old charge records
clear_charge_records()


# 3. Extract charges from PDF
charges = extract_charges(pdf_path)


print("\nExtracted Charges:")
print("-----------------------------")
print(charges.to_string(index=False))


# 4. Store charges
insert_charge_records(charges)

print("\nCharges inserted successfully!")


# 5. Read them back from database
stored_charges = get_charge_records()


print("\nCharges from Database:")
print("-----------------------------")

for charge in stored_charges:

    print(charge)