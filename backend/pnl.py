# =========================================
# UNREALISED P&L CALCULATION
# =========================================


def calculate_unrealised_pnl(
    remaining_lots,
    current_prices
):
    """
    Calculate unrealised P&L for remaining FIFO lots.

    If a stock's current market price is missing,
    its market value and unrealised P&L are returned
    as None instead of treating the price as ₹0.

    Returns:
        holdings:
            Stock-wise portfolio details.

        total_unrealised:
            Total unrealised P&L for stocks that have
            a valid current market price.
    """

    holdings = []

    total_unrealised = 0.0


    # =========================================
    # PROCESS EACH STOCK
    # =========================================

    for stock, lots in remaining_lots.items():

        total_quantity = 0.0

        fifo_cost = 0.0


        # -------------------------------------
        # PROCESS FIFO LOTS
        # -------------------------------------

        for lot in lots:

            quantity = float(
                lot.get("quantity", 0)
            )

            base_price = float(
                lot.get("price", 0)
            )


            # BUY charge per share
            charge_per_share = float(
                lot.get(
                    "charge_per_share",
                    0
                )
            )


            # Adjusted acquisition price
            adjusted_price = (
                base_price +
                charge_per_share
            )


            # Total quantity
            total_quantity += quantity


            # Total acquisition cost
            fifo_cost += (
                quantity *
                adjusted_price
            )


        # -------------------------------------
        # Ignore empty lots
        # -------------------------------------

        if total_quantity <= 0:
            continue


        # =========================================
        # GET CURRENT MARKET PRICE
        # =========================================

        price_value = current_prices.get(stock)


        if price_value is None:

            # No market price supplied
            current_price = None

        else:

            try:

                current_price = float(
                    price_value
                )

            except (TypeError, ValueError):

                current_price = None


        # =========================================
        # CALCULATE MARKET VALUE AND P&L
        # =========================================

        if current_price is None:

            market_value = None

            unrealised = None

        else:

            market_value = (
                total_quantity *
                current_price
            )

            unrealised = (
                market_value -
                fifo_cost
            )

            total_unrealised += unrealised


        # =========================================
        # FORMAT QUANTITY
        # =========================================

        if total_quantity.is_integer():

            display_quantity = int(
                total_quantity
            )

        else:

            display_quantity = total_quantity


        # =========================================
        # ADD HOLDING
        # =========================================

        holdings.append({

            "Stock":
                stock,

            "Quantity":
                display_quantity,

            "FIFO Cost":
                fifo_cost,

            "Current Price":
                current_price,

            "Market Value":
                market_value,

            "Unrealised P&L":
                unrealised

        })


    return (
        holdings,
        total_unrealised
    )


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    remaining_lots = {

        "ALPHA": [

            {
                "quantity": 20,
                "price": 100,
                "charge_per_share": 0.10
            }

        ],

        "BETA": [

            {
                "quantity": 50,
                "price": 60,
                "charge_per_share": 0
            }

        ]

    }


    # =====================================
    # TEST 1: NORMAL PRICES
    # =====================================

    current_prices = {

        "ALPHA": 140,

        "BETA": 80

    }


    print("\nMARKET PRICE TEST - NORMAL")

    print("=" * 60)


    holdings, total_pnl = (
        calculate_unrealised_pnl(
            remaining_lots,
            current_prices
        )
    )


    for holding in holdings:

        print(holding)


    print(
        "\nTotal Unrealised P&L:",
        round(total_pnl, 2)
    )


    # =====================================
    # TEST 2: MISSING BETA PRICE
    # =====================================

    current_prices = {

        "ALPHA": 140

    }


    print("\nMARKET PRICE TEST - MISSING PRICE")

    print("=" * 60)


    holdings, total_pnl = (
        calculate_unrealised_pnl(
            remaining_lots,
            current_prices
        )
    )


    for holding in holdings:

        print(holding)


    print(
        "\nTotal Unrealised P&L:",
        round(total_pnl, 2)
    )


    # =====================================
    # TEST 3: ZERO PRICE
    # =====================================

    current_prices = {

        "ALPHA": 0,

        "BETA": 80

    }


    print("\nMARKET PRICE TEST - ZERO PRICE")

    print("=" * 60)


    holdings, total_pnl = (
        calculate_unrealised_pnl(
            remaining_lots,
            current_prices
        )
    )


    for holding in holdings:

        print(holding)


    print(
        "\nTotal Unrealised P&L:",
        round(total_pnl, 2)
    )