from collections import deque


def calculate_fifo(
    trades,
    existing_lots=None,
    charge_records=None
):

    # Convert DataFrame to list of dictionaries
    if hasattr(trades, "to_dict"):
        trades = trades.to_dict("records")

    # Use existing FIFO lots if provided
    lots = (
        existing_lots
        if existing_lots is not None
        else {}
    )

    realised_profit = 0

    matches = []


    # =========================================
    # BUY CHARGE RECORDS
    # =========================================

    buy_charges = []

    if charge_records:

        buy_charges = [
            charge
            for charge in charge_records
            if charge["Type"].upper() == "BUY"
        ]


    # Keep track of which BUY charge belongs
    # to the next BUY transaction for each stock
    buy_charge_position = {}


    # =========================================
    # PROCESS TRADES
    # =========================================

    for trade in trades:

        stock = trade["Stock"]

        trade_type = trade["Type"].upper()

        quantity = int(
            trade["Quantity"]
        )

        price = float(
            trade["Price"]
        )


        # Create FIFO queue for new stock
        if stock not in lots:

            lots[stock] = deque()


        # =====================================
        # BUY
        # =====================================

        if trade_type == "BUY":

            buy_charge = 0


            # Find BUY charges for this stock
            stock_buy_charges = [
                charge
                for charge in buy_charges
                if charge["Stock"] == stock
            ]


            position = buy_charge_position.get(
                stock,
                0
            )


            # Get the correct BUY charge
            if position < len(stock_buy_charges):

                charge = stock_buy_charges[position]

                buy_charge = float(
                    charge["Total Charges"]
                )

                buy_charge_position[stock] = (
                    position + 1
                )


            # BUY charge per share
            charge_per_share = (
                buy_charge / quantity
                if quantity > 0
                else 0
            )


            # Store charge information
            # inside the FIFO lot
            lots[stock].append({

                "quantity": quantity,

                "price": price,

                "buy_charge": buy_charge,

                "charge_per_share":
                    charge_per_share

            })


        # =====================================
        # SELL
        # =====================================

        elif trade_type == "SELL":

            sell_quantity = quantity


            while sell_quantity > 0:

                # No shares available
                if not lots[stock]:

                    raise ValueError(
                        f"Not enough {stock} shares "
                        f"to complete SELL."
                    )


                # Get oldest BUY lot
                oldest_lot = lots[stock][0]


                # Quantity matched from this lot
                matched_quantity = min(

                    sell_quantity,

                    oldest_lot["quantity"]

                )


                # =================================
                # BUY-SIDE CHARGE
                # =================================

                charge_per_share = (
                    oldest_lot.get(
                        "charge_per_share",
                        0
                    )
                )


                buy_charge_for_match = (
                    charge_per_share *
                    matched_quantity
                )


                # Adjusted BUY price
                adjusted_buy_price = (
                    oldest_lot["price"] +
                    charge_per_share
                )


                # =================================
                # P&L AFTER BUY CHARGES
                # =================================

                profit = (

                    price -
                    adjusted_buy_price

                ) * matched_quantity


                realised_profit += profit


                # =================================
                # SAVE FIFO MATCH
                # =================================

                matches.append({

                    "Stock":
                        stock,

                    "Buy Price":
                        oldest_lot["price"],

                    "Adjusted Buy Price":
                        adjusted_buy_price,

                    "Sell Price":
                        price,

                    "Quantity":
                        matched_quantity,

                    "Buy Charges":
                        buy_charge_for_match,

                    "Gross P&L":
                        profit

                })


                # =================================
                # REDUCE FIFO LOT
                # =================================

                oldest_lot["quantity"] -= (
                    matched_quantity
                )


                sell_quantity -= (
                    matched_quantity
                )


                # Remove lot if fully consumed
                if oldest_lot["quantity"] == 0:

                    lots[stock].popleft()


        else:

            raise ValueError(
                f"Unknown trade type: {trade_type}"
            )


    return (
        realised_profit,
        lots,
        matches
    )


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    trades = [

        {
            "Stock": "ALPHA",
            "Type": "BUY",
            "Quantity": 100,
            "Price": 100
        },

        {
            "Stock": "ALPHA",
            "Type": "SELL",
            "Quantity": 30,
            "Price": 130
        },

        {
            "Stock": "ALPHA",
            "Type": "SELL",
            "Quantity": 70,
            "Price": 130
        }

    ]


    charge_records = [

        {
            "Stock": "ALPHA",
            "Type": "BUY",
            "Quantity": 100,
            "Total Charges": 10
        }

    ]


    profit, remaining_lots, matches = calculate_fifo(

        trades,

        charge_records=charge_records

    )


    print("PARTIAL BUY CHARGE TEST")
    print("=" * 50)


    total_buy_charges = 0
    total_profit = 0


    for match in matches:

        print(
            "\nStock:",
            match["Stock"]
        )

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


    print("\n" + "=" * 50)

    print(
        "Total BUY Charges:",
        total_buy_charges
    )

    print(
        "Total P&L after BUY Charges:",
        total_profit
    )


    print("\nRemaining Lots:")

    for stock, lots in remaining_lots.items():

        print(stock)

        for lot in lots:

            print(lot)