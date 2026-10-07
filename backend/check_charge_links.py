from database import (
    get_all_transactions,
    get_charge_records
)


transactions = get_all_transactions()

charge_records = get_charge_records()


print("\nTRANSACTION IDs")
print("=" * 60)

for transaction in transactions:

    print(
        "ID:",
        transaction["id"],
        "|",
        transaction["Type"],
        "|",
        transaction["Stock"],
        "| Qty:",
        transaction["Quantity"]
    )


print("\nCHARGE TRANSACTION IDs")
print("=" * 60)

for charge in charge_records:

    print(
        "Charge ID:",
        charge["id"],
        "|",
        charge["Type"],
        "|",
        charge["Stock"],
        "| Qty:",
        charge["Quantity"],
        "| Transaction ID:",
        charge.get("Transaction ID"),
        "| Total:",
        charge["Total Charges"]
    )