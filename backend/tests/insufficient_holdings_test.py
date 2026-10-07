from fifo import calculate_fifo


# =========================================
# TEST TRANSACTIONS
# =========================================

trades = [

    {
        "Stock": "ALPHA",
        "Type": "BUY",
        "Quantity": 50,
        "Price": 100
    },

    {
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 80,
        "Price": 120
    }

]


# =========================================
# RUN TEST
# =========================================

print("\nINSUFFICIENT HOLDINGS TEST")
print("=" * 60)


try:

    profit, remaining_lots, matches = calculate_fifo(
        trades
    )

    print(
        "Unexpected result: SELL was accepted."
    )

    print(
        "Realised P&L:",
        profit
    )


except ValueError as error:

    print(
        "Correctly rejected:"
    )

    print(
        error
    )