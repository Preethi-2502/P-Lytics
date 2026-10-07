from charges import apply_buy_charges_to_matches


matches = [

    {
        "Stock": "ALPHA",
        "Buy Price": 100,
        "Sell Price": 130,
        "Quantity": 80,
        "Gross P&L": 2400
    },

    {
        "Stock": "ALPHA",
        "Buy Price": 110,
        "Sell Price": 130,
        "Quantity": 20,
        "Gross P&L": 400
    }

]


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
    }

]


updated_matches = apply_buy_charges_to_matches(
    matches,
    charge_records
)


print("BUY CHARGE FIFO TEST")
print("=" * 50)


total_profit = 0


for match in updated_matches:

    print("\nStock:", match["Stock"])
    print("Quantity:", match["Quantity"])
    print("Original Buy Price:", match["Buy Price"])
    print("Adjusted Buy Price:", match["Adjusted Buy Price"])
    print("Buy Charge Applied:", match["Buy Charge Applied"])
    print(
        "P&L After Buy Charges:",
        match["Gross P&L After Buy Charges"]
    )

    total_profit += (
        match["Gross P&L After Buy Charges"]
    )


print("\n" + "=" * 50)

print(
    "Total P&L After BUY Charges:",
    total_profit
)