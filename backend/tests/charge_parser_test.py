from pathlib import Path

from pdf_parser import extract_charges


# Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Sample PDF
pdf_path = project_folder / "sample_contract_note_equity_project.pdf"


# Extract charges
charges = extract_charges(pdf_path)


print("\nExtracted Charges")
print("-----------------------------")

print(charges.to_string(index=False))