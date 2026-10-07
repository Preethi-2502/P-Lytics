def calculate_net_pnl(gross_pnl, brokerage, stt, other_charges):

    total_charges = brokerage + stt + other_charges

    net_pnl = gross_pnl - total_charges

    return total_charges, net_pnl

def allocate_sell_charges(sell_quantity, charges, matched_quantities):
    """
    Allocate the charges of one SELL transaction
    across the FIFO matched quantities.

    Example:
    SELL 130 shares
    Total charges = ₹26

    FIFO matches:
    100 shares
    30 shares
    """

    allocated_charges = []

    for matched_quantity in matched_quantities:

        allocated = (
            charges * matched_quantity / sell_quantity
        )

        allocated_charges.append(allocated)

    return allocated_charges
def apply_sell_charges_to_matches(
    matches,
    charge_records
):

    # =========================================
    # BUILD SELL CHARGE LOOKUP
    # =========================================

    sell_charge_lookup = {}

    for charge in charge_records:

        if charge["Type"].upper() != "SELL":
            continue

        transaction_id = charge.get(
            "Transaction ID"
        )

        if transaction_id is not None:

            sell_charge_lookup[
                transaction_id
            ] = charge


    # =========================================
    # GROUP FIFO MATCHES BY SELL TRANSACTION
    # =========================================

    sell_groups = {}

    for match in matches:

        sell_transaction_id = match.get(
            "Sell Transaction ID"
        )

        if sell_transaction_id not in sell_groups:

            sell_groups[
                sell_transaction_id
            ] = []

        sell_groups[
            sell_transaction_id
        ].append(match)


    updated_matches = []


    # =========================================
    # PROCESS EACH SELL TRANSACTION
    # =========================================

    for sell_transaction_id, group in sell_groups.items():

        charge = sell_charge_lookup.get(
            sell_transaction_id
        )


        # -------------------------------------
        # No matching SELL charge
        # -------------------------------------

        if charge is None:

            for match in group:

                updated_match = match.copy()

                updated_match[
                    "Allocated Charges"
                ] = 0

                updated_match[
                    "Net P&L"
                ] = match["Gross P&L"]

                updated_matches.append(
                    updated_match
                )

            continue


        # -------------------------------------
        # Get total charge for this SELL
        # -------------------------------------

        sell_quantity = int(
            charge["Quantity"]
        )

        total_sell_charges = float(
            charge["Total Charges"]
        )


        # -------------------------------------
        # Calculate matched quantity
        # -------------------------------------

        total_matched_quantity = sum(

            int(match["Quantity"])

            for match in group

        )


        if total_matched_quantity <= 0:

            continue


        # =====================================
        # ALLOCATE SELL CHARGES
        # =====================================

        for match in group:

            matched_quantity = int(
                match["Quantity"]
            )


            allocated_charge = (

                total_sell_charges
                * matched_quantity
                / sell_quantity

            )


            # ---------------------------------
            # Net P&L
            # ---------------------------------

            net_pnl = (

                match["Gross P&L"]
                - allocated_charge

            )


            updated_match = match.copy()


            updated_match[
                "Allocated Charges"
            ] = allocated_charge


            updated_match[
                "Net P&L"
            ] = net_pnl


            updated_matches.append(
                updated_match
            )


    return updated_matches
def apply_buy_charges_to_matches(
    matches,
    charge_records
):

    # Get BUY charge records
    buy_charges = [
        charge
        for charge in charge_records
        if charge["Type"].upper() == "BUY"
    ]

    # Keep track of the next BUY charge for each stock
    charge_position = {}

    updated_matches = []

    for match in matches:

        stock = match["Stock"]
        matched_quantity = match["Quantity"]

        # Find BUY charges for this stock
        stock_charges = [
            charge
            for charge in buy_charges
            if charge["Stock"] == stock
        ]

        position = charge_position.get(
            stock,
            0
        )

        # Find the BUY charge that created this FIFO lot
        if position < len(stock_charges):

            charge = stock_charges[position]

            charge_quantity = int(
                charge["Quantity"]
            )

            total_charge = float(
                charge["Total Charges"]
            )

            charge_per_share = (
                total_charge /
                charge_quantity
            )

            # Adjust the BUY cost
            adjusted_buy_price = (
                match["Buy Price"] +
                charge_per_share
            )

            charge_position[stock] = position + 1

        else:

            adjusted_buy_price = (
                match["Buy Price"]
            )

            total_charge = 0


        # Calculate P&L after BUY charges
        adjusted_profit = (
            match["Sell Price"] -
            adjusted_buy_price
        ) * matched_quantity


        updated_match = match.copy()

        updated_match["Buy Charges Per Share"] = (
            adjusted_buy_price -
            match["Buy Price"]
        )

        updated_match["Adjusted Buy Price"] = (
            adjusted_buy_price
        )

        updated_match["Buy Charge Applied"] = (
            total_charge
        )

        updated_match["Gross P&L After Buy Charges"] = (
            adjusted_profit
        )

        updated_matches.append(
            updated_match
        )

    return updated_matches
if __name__ == "__main__":

    sell_quantity = 130

    total_charges = 26

    matched_quantities = [
        100,
        30
    ]

    allocated = allocate_sell_charges(
        sell_quantity,
        total_charges,
        matched_quantities
    )

    print("Original Charges:", total_charges)

    print("Allocated Charges:")

    for charge in allocated:
        print("₹", round(charge, 2))

    print(
        "Total Allocated:",
        round(sum(allocated), 2)
    )