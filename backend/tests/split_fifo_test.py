from portfolio_engine import process_events


events = [

    {
        "Date": "2026-09-01",
        "Stock": "ALPHA",
        "Type": "BUY",
        "Quantity": 100,
        "Price": 200
    },

    {
        "Date": "2026-09-05",
        "Stock": "ALPHA",
        "Type": "SPLIT",
        "Old Shares": 1,
        "New Shares": 2
    },

    {
        "Date": "2026-09-10",
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 50,
        "Price": 120
    }

]


print("\nSTOCK SPLIT FIFO TEST")
print("=" * 60)


profit, remaining_lots, matches = process_events(
    events
)


print(
    "Realised P&L:",
    profit
)


print("\nFIFO Matches:")

for match in matches:

    print(match)


print("\nRemaining Lots:")

for stock, lots in remaining_lots.items():

    print(stock)

    for lot in lots:

        print(
            "Quantity:",
            lot["quantity"],
            "Price:",
            lot["price"]
        )