from database import (
    get_all_transactions,
    get_corporate_actions
)

from portfolio_engine import (
    build_portfolio_events,
    process_events
)


# Get data from database
transactions = get_all_transactions()

corporate_actions = get_corporate_actions()


# Build all events
events = build_portfolio_events(
    transactions,
    corporate_actions
)


print("\nAll Portfolio Events")
print("=" * 50)

for event in sorted(
    events,
    key=lambda x: x["Date"]
):

    print(event)


# Process events
realised_profit, remaining_lots, matches = process_events(
    events
)


print("\nPortfolio Result")
print("=" * 50)

print(
    "Realised P&L:",
    realised_profit
)


print("\nFIFO Matches:")

for match in matches:
    print(match)


print("\nRemaining Holdings:")

for stock, lots in remaining_lots.items():

    print(stock)

    for lot in lots:

        print(
            "  Quantity:",
            lot["quantity"],
            "Price:",
            lot["price"]
        )