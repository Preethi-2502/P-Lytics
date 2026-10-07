from pnl import calculate_unrealised_pnl


# =========================================
# REMAINING HOLDINGS
# =========================================

remaining_lots = {

    "ALPHA": [
        {
            "quantity": 20,
            "price": 100
        }
    ],

    "BETA": [
        {
            "quantity": 50,
            "price": 60
        }
    ]

}


# =========================================
# TEST 1: NORMAL PRICES
# =========================================

current_prices = {

    "ALPHA": 140,

    "BETA": 80

}


print("\nMARKET PRICE TEST - NORMAL")
print("=" * 50)


holdings, total_pnl = calculate_unrealised_pnl(
    remaining_lots,
    current_prices
)


for holding in holdings:
    print(holding)


print(
    "\nTotal Unrealised P&L:",
    total_pnl
)


# =========================================
# TEST 2: MISSING BETA PRICE
# =========================================

current_prices = {

    "ALPHA": 140

}


print("\nMARKET PRICE TEST - MISSING PRICE")
print("=" * 50)


holdings, total_pnl = calculate_unrealised_pnl(
    remaining_lots,
    current_prices
)


for holding in holdings:
    print(holding)


print(
    "\nTotal Unrealised P&L:",
    total_pnl
)


# =========================================
# TEST 3: ZERO PRICE
# =========================================

current_prices = {

    "ALPHA": 0,

    "BETA": 80

}


print("\nMARKET PRICE TEST - ZERO PRICE")
print("=" * 50)


holdings, total_pnl = calculate_unrealised_pnl(
    remaining_lots,
    current_prices
)


for holding in holdings:
    print(holding)


print(
    "\nTotal Unrealised P&L:",
    total_pnl
)