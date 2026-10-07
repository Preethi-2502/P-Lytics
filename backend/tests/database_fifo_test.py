from database import get_transactions
from fifo import calculate_fifo


# Read transactions from database
transactions = get_transactions()

print("Transactions from Database:")
print("--------------------------------")

for trade in transactions:
    print(trade)


# Send database data to FIFO
realised_profit, remaining_lots , matches = calculate_fifo(transactions)


print("\nFIFO RESULT")
print("--------------------------------")

print("Realised Profit:", realised_profit)

print("\nRemaining Lots:")

for stock, lots in remaining_lots.items():

    print(stock)

    for lot in lots:
        print(
            "Quantity:", lot["quantity"],
            "Price:", lot["price"]
        )