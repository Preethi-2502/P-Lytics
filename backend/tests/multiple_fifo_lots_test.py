from fifo import calculate_fifo
from charges import apply_sell_charges_to_matches


# =========================================
# TRANSACTIONS
# =========================================

trades = [

    {
        "Stock": "ALPHA",
        "Type": "BUY",
        "Quantity": 100,
        "Price": 100
    },

    {
        "Stock": "ALPHA",
        "Type": "BUY",
        "Quantity": 50,
        "Price": 110
    },

    {
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 130,
        "Price": 150
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
        "Total Charges": 10
    },

    {
        "Stock": "ALPHA",
        "Type": "BUY",
        "Quantity": 50,
        "Total Charges": 5
    },

    {
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 130,
        "Total Charges": 26
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
# APPLY SELL CHARGES
# =========================================

updated_matches = apply_sell_charges_to_matches(
    matches,
    charge_records
)


# =========================================
# DISPLAY RESULTS
# =========================================

print("\nMULTIPLE FIFO LOTS TEST")
print("=" * 70)


total_net_pnl = 0


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

    print("Gross P&L:",
          match["Gross P&L"])

    print("Net P&L:",
          match["Net P&L"])

    total_net_pnl += match["Net P&L"]


print("\n" + "=" * 70)

print(
    "Total Net P&L:",
    total_net_pnl
)


# =========================================
# REMAINING LOTS
# =========================================

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