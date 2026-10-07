from fifo import calculate_fifo
from charges import apply_sell_charges_to_matches


# =========================================
# TEST TRANSACTIONS
# =========================================

trades = [

    {
        "Stock": "ALPHA",
        "Type": "BUY",
        "Quantity": 100,
        "Price": 150
    },

    {
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 40,
        "Price": 120
    }

]


# =========================================
# CHARGE RECORDS
# =========================================

charge_records = [

    {
        "Stock": "ALPHA",
        "Type": "BUY",
        "Quantity": 100,
        "Total Charges": 10,
        "Transaction ID": 1
    },

    {
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 40,
        "Total Charges": 5,
        "Transaction ID": 2
    }

]


# =========================================
# RUN FIFO
# =========================================

profit, remaining_lots, matches = calculate_fifo(
    trades,
    charge_records=charge_records
)


# =========================================
# ADD SELL CHARGES
# =========================================

updated_matches = apply_sell_charges_to_matches(
    matches,
    charge_records
)


# =========================================
# DISPLAY RESULTS
# =========================================

print("\nLOSS-MAKING TRADE TEST")
print("=" * 60)


for match in updated_matches:

    print("\nStock:",
          match["Stock"])

    print("Quantity:",
          match["Quantity"])

    print("Buy Price:",
          match["Buy Price"])

    print("Adjusted Buy Price:",
          match["Adjusted Buy Price"])

    print("Sell Price:",
          match["Sell Price"])

    print("BUY Charges:",
          match["Buy Charges"])

    print("SELL Charges:",
          match["Allocated Charges"])

    print("Net P&L:",
          match["Net P&L"])


print("\n" + "=" * 60)

total_net_pnl = sum(
    match["Net P&L"]
    for match in updated_matches
)

print(
    "Total Net P&L:",
    total_net_pnl
)


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