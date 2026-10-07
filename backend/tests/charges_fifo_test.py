from fifo import calculate_fifo
from charges import allocate_sell_charges


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


# Run FIFO
realised_profit, remaining_lots, matches = calculate_fifo(
    trades
)


# Total SELL charges
sell_charges = 26


# Get matched quantities
matched_quantities = []

for match in matches:

    matched_quantities.append(
        match["Quantity"]
    )


# Allocate charges
allocated_charges = allocate_sell_charges(
    130,
    sell_charges,
    matched_quantities
)


print("FIFO Matches with Charges")
print("--------------------------------")


total_net_profit = 0


for i in range(len(matches)):

    match = matches[i]

    charge = allocated_charges[i]

    net_profit = (
        match["Gross P&L"] - charge
    )

    total_net_profit += net_profit


    print(
        "Quantity:",
        match["Quantity"]
    )

    print(
        "Buy Price:",
        match["Buy Price"]
    )

    print(
        "Sell Price:",
        match["Sell Price"]
    )

    print(
        "Gross P&L:",
        match["Gross P&L"]
    )

    print(
        "Allocated Charge:",
        charge
    )

    print(
        "Net P&L:",
        net_profit
    )

    print("--------------------------------")


print(
    "Total Gross P&L:",
    realised_profit
)

print(
    "Total Charges:",
    sum(allocated_charges)
)

print(
    "Total Net P&L:",
    total_net_profit
)