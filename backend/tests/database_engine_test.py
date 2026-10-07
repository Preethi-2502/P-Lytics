from database import (
    get_all_transactions,
    get_corporate_actions
)

from portfolio_engine import process_events


# =================================
# CONVERT DATE
# =================================

def clean_date(value):

    return str(value)[:10]


# =================================
# GET TRANSACTIONS
# =================================

transactions = get_all_transactions()


# =================================
# GET CORPORATE ACTIONS
# =================================

corporate_actions = get_corporate_actions()


# =================================
# BUILD COMBINED EVENTS
# =================================

events = []


# Normal BUY / SELL transactions
for trade in transactions:

    events.append({

        "Date":
            clean_date(trade["Date"]),

        "Stock":
            trade["Stock"],

        "Type":
            trade["Type"],

        "Quantity":
            trade["Quantity"],

        "Price":
            trade["Price"]

    })


# Corporate actions
for action in corporate_actions:

    action_type = action["Type"].upper()

    if action_type == "SPLIT":

        events.append({

            "Date":
                clean_date(action["Date"]),

            "Stock":
                action["Stock"],

            "Type":
                "SPLIT",

            "Old Shares":
                action["Old Shares"],

            "New Shares":
                action["New Shares"]

        })

    elif action_type == "BONUS":

        events.append({

            "Date":
                clean_date(action["Date"]),

            "Stock":
                action["Stock"],

            "Type":
                "BONUS",

            "Bonus For":
                action["Old Shares"],

            "Bonus Receive":
                action["New Shares"]

        })


# =================================
# DISPLAY EVENTS
# =================================

print("\nCombined Portfolio Events")
print("=" * 50)

for event in sorted(
    events,
    key=lambda x: x["Date"]
):

    print(event)


# =================================
# PROCESS EVENTS
# =================================

realised_profit, remaining_lots, matches = (
    process_events(events)
)


# =================================
# DISPLAY RESULT
# =================================

print("\nPortfolio Engine Result")
print("=" * 50)

print(
    "Realised P&L:",
    realised_profit
)


print("\nFIFO Matches:")

for match in matches:

    print(match)


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