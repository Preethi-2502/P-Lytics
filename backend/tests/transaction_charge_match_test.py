from charges import apply_sell_charges_to_matches


# =========================================
# FIFO MATCHES
# =========================================

matches = [

    {
        "Stock": "ALPHA",
        "Buy Price": 100,
        "Adjusted Buy Price": 100.10,
        "Sell Price": 130,
        "Quantity": 50,
        "Gross P&L": 1495.00,
        "Buy Charges": 5.00,
        "Buy Transaction ID": 1,
        "Sell Transaction ID": 3
    },

    {
        "Stock": "ALPHA",
        "Buy Price": 110,
        "Adjusted Buy Price": 110.10,
        "Sell Price": 130,
        "Quantity": 30,
        "Gross P&L": 597.00,
        "Buy Charges": 3.00,
        "Buy Transaction ID": 2,
        "Sell Transaction ID": 4
    }

]


# =========================================
# SELL CHARGES
# =========================================

charge_records = [

    {
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 50,
        "Total Charges": 10.00,
        "Transaction ID": 3
    },

    {
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 30,
        "Total Charges": 6.00,
        "Transaction ID": 4
    }

]


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

print("\nTRANSACTION-SPECIFIC CHARGE TEST")
print("=" * 60)


total_net_pnl = 0


for match in updated_matches:

    print("\nStock:",
          match["Stock"])

    print("Sell Transaction ID:",
          match["Sell Transaction ID"])

    print("Quantity:",
          match["Quantity"])

    print("Gross P&L:",
          match["Gross P&L"])

    print("Allocated SELL Charges:",
          match["Allocated Charges"])

    print("Net P&L:",
          match["Net P&L"])


    total_net_pnl += match["Net P&L"]


# =========================================
# TOTAL
# =========================================

print("\n" + "=" * 60)

print(
    "Total Net P&L:",
    total_net_pnl
)