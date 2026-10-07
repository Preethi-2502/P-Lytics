from fifo import calculate_fifo
from corporate_actions import apply_split_to_lots


# --------------------------------
# BUY 100 shares @ ₹200
# --------------------------------

trades = [
    {
        "Stock": "ALPHA",
        "Type": "BUY",
        "Quantity": 100,
        "Price": 200
    }
]


realised_profit, remaining_lots, matches = calculate_fifo(
    trades
)


print("Before Split:")
print(dict(remaining_lots))


# --------------------------------
# Apply 1:2 split
# --------------------------------

alpha_lots = list(
    remaining_lots["ALPHA"]
)

alpha_lots = apply_split_to_lots(
    alpha_lots,
    old_shares=1,
    new_shares=2
)

remaining_lots["ALPHA"] = alpha_lots


print("\nAfter Split:")
print(dict(remaining_lots))


# --------------------------------
# SELL 50 shares @ ₹120
# --------------------------------

sell_trade = [
    {
        "Stock": "ALPHA",
        "Type": "SELL",
        "Quantity": 50,
        "Price": 120
    }
]


realised_profit, remaining_lots, matches = calculate_fifo(
    sell_trade,
    existing_lots=remaining_lots
)


print("\nSELL Result:")
print("Realised Profit:", realised_profit)

print("\nFIFO Match:")

for match in matches:
    print(match)

print("\nRemaining Lots:")
print(dict(remaining_lots))