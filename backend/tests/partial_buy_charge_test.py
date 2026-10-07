from fifo import calculate_fifo


# =========================================
# TEST TRANSACTIONS
# =========================================

trades = [

    # Buy 100 ALPHA shares at ₹100
    {
        "Stock": "ALPHA",
        "Type": "BUY",
        "Quantity": 100,
        "Price": 100
    },

    # Sell first 30 shares at ₹130
    {
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 30,
        "Price": 130
    },

    # Sell remaining 70 shares at ₹130
    {
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 70,
        "Price": 130
    }
]


# =========================================
# BUY CHARGE
# =========================================

charge_records = [

    {
        "Stock": "ALPHA",
        "Type": "BUY",
        "Quantity": 100,
        "Total Charges": 10
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
# DISPLAY RESULTS
# =========================================

print("\nPARTIAL BUY CHARGE TEST")
print("=" * 50)


total_buy_charges = 0
total_profit = 0


for match in matches:

    print("\nStock:", match["Stock"])

    print(
        "Quantity:",
        match["Quantity"]
    )

    print(
        "Original Buy Price:",
        match["Buy Price"]
    )

    print(
        "Adjusted Buy Price:",
        match["Adjusted Buy Price"]
    )

    print(
        "BUY Charge for Match:",
        match["Buy Charges"]
    )

    print(
        "P&L after BUY charge:",
        match["Gross P&L"]
    )

    total_buy_charges += (
        match["Buy Charges"]
    )

    total_profit += (
        match["Gross P&L"]
    )


# =========================================
# TOTALS
# =========================================

print("\n" + "=" * 50)

print(
    "Total BUY Charges:",
    total_buy_charges
)

print(
    "Total P&L after BUY Charges:",
    total_profit
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
            lot["price"],
            "BUY Charge:",
            lot.get("buy_charge", 0)
        )