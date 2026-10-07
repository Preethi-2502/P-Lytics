from pathlib import Path
import pdfplumber
import pandas as pd


def extract_transactions(pdf_path):

    transactions = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            for table in tables:

                for row in table:

                    # Skip empty rows
                    if not row:
                        continue

                    # Clean empty cells
                    row = [cell.strip() if cell else "" for cell in row]

                    # We need at least 8 columns
                    if len(row) < 8:
                        continue

                    # Check whether this is a BUY/SELL trade row
                    if row[4] not in ["BUY", "SELL"]:
                        continue

                    try:
                        transaction = {
                            "Date": pd.to_datetime(row[1]),
                            "Stock": row[2],
                            "Type": row[4],
                            "Quantity": int(row[5].replace(",", "")),
                            "Price": float(row[6].replace(",", ""))
                        }

                        transactions.append(transaction)

                    except ValueError:
                        # Ignore rows that contain invalid data
                        continue

    return pd.DataFrame(transactions)
def extract_charges(pdf_path):

    charges = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            for table in tables:

                if not table:
                    continue

                # Check whether this is the Charges table
                first_row = table[0]

                if not first_row:
                    continue

                first_cell = str(first_row[0]).strip().lower()

                if first_cell != "transaction":
                    continue

                # Read each charge row
                for row in table[1:]:

                    if not row or len(row) < 7:
                        continue

                    try:

                        transaction_text = row[0].strip()

                        parts = transaction_text.split()

                        stock = parts[0]
                        trade_type = parts[1]
                        quantity = int(parts[2])

                        brokerage = float(
                            row[1].replace(",", "")
                        )

                        stt = float(
                            row[2].replace(",", "")
                        )

                        exchange_charges = float(
                            row[3].replace(",", "")
                        )

                        gst = float(
                            row[4].replace(",", "")
                        )

                        other_charges = float(
                            row[5].replace(",", "")
                        )

                        total_charges = float(
                            row[6].replace(",", "")
                        )

                        charges.append({

                            "Stock": stock,

                            "Type": trade_type,

                            "Quantity": quantity,

                            "Brokerage": brokerage,

                            "STT": stt,

                            "Exchange Charges":
                                exchange_charges,

                            "GST": gst,

                            "Other Charges":
                                other_charges,

                            "Total Charges":
                                total_charges

                        })

                    except (ValueError, IndexError):

                        continue

    return pd.DataFrame(charges)


if __name__ == "__main__":

    project_folder = Path(__file__).resolve().parent.parent

    pdf_path = project_folder / "sample_contract_note_equity_project.pdf"

    print("Reading PDF:")
    print(pdf_path)

    df = extract_transactions(pdf_path)

    print("\nExtracted Transactions:")
    print(df.to_string(index=False))