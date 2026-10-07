from collections import deque
from datetime import datetime

from corporate_actions import (
    apply_bonus_to_lots,
    apply_split_to_lots
)


# =========================================
# BUILD COMBINED PORTFOLIO EVENTS
# =========================================

def build_portfolio_events(
    transactions,
    corporate_actions
):

    events = []

    # -----------------------------
    # BUY / SELL transactions
    # -----------------------------

    for trade in transactions:

        events.append({

            "Date":
                str(trade["Date"])[:10],

            "Stock":
                trade["Stock"],

            "Type":
                trade["Type"].upper(),

            "Quantity":
                trade["Quantity"],

            "Price":
                trade["Price"],

            "Transaction ID":
                trade["id"]

        })


    # -----------------------------
    # Corporate actions
    # -----------------------------

    for action in corporate_actions:

        action_type = action["Type"].upper()

        # STOCK SPLIT
        if action_type == "SPLIT":

            events.append({

                "Date":
                    str(action["Date"])[:10],

                "Stock":
                    action["Stock"],

                "Type":
                    "SPLIT",

                "Old Shares":
                    action["Old Shares"],

                "New Shares":
                    action["New Shares"]

            })


        # BONUS
        elif action_type == "BONUS":

            events.append({

                "Date":
                    str(action["Date"])[:10],

                "Stock":
                    action["Stock"],

                "Type":
                    "BONUS",

                "Bonus For":
                    action["Old Shares"],

                "Bonus Receive":
                    action["New Shares"]

            })


    return events


# =========================================
# PROCESS PORTFOLIO EVENTS
# =========================================

def process_events(
    events,
    charge_records=None
):

    if charge_records is None:
        charge_records = []


    # =====================================
    # BUY CHARGE LOOKUP
    # =====================================

    buy_charge_lookup = {}

    for charge in charge_records:

        if charge["Type"].upper() != "BUY":
            continue

        transaction_id = charge.get(
            "Transaction ID"
        )

        if transaction_id is not None:

            buy_charge_lookup[
                transaction_id
            ] = charge


    # =====================================
    # SORT EVENTS BY DATE
    # =====================================

    events = sorted(

        events,

        key=lambda event:
            datetime.strptime(
                str(event["Date"])[:10],
                "%Y-%m-%d"
            )

    )


    # =====================================
    # FIFO LOTS
    # =====================================

    lots = {}

    realised_profit = 0

    matches = []


    # =====================================
    # PROCESS EACH EVENT
    # =====================================

    for event in events:

        stock = event["Stock"]

        event_type = event["Type"].upper()


        # Create FIFO queue
        if stock not in lots:

            lots[stock] = deque()


        # =================================
        # BUY
        # =================================

        if event_type == "BUY":

            quantity = int(
                event["Quantity"]
            )

            price = float(
                event["Price"]
            )

            transaction_id = event.get(
                "Transaction ID"
            )


            # -----------------------------
            # Find exact BUY charge
            # -----------------------------

            charge = buy_charge_lookup.get(
                transaction_id
            )


            buy_charge = 0


            if charge:

                buy_charge = float(
                    charge["Total Charges"]
                )


            # -----------------------------
            # Charge per share
            # -----------------------------

            charge_per_share = (

                buy_charge / quantity

                if quantity > 0

                else 0

            )


            # -----------------------------
            # Create FIFO lot
            # -----------------------------

            lots[stock].append({

                "quantity":
                    quantity,

                "price":
                    price,

                "buy_charge":
                    buy_charge,

                "charge_per_share":
                    charge_per_share,

                "Transaction ID":
                    transaction_id

            })


        # =================================
        # SELL
        # =================================

        elif event_type == "SELL":

            sell_quantity = int(
                event["Quantity"]
            )

            sell_price = float(
                event["Price"]
            )

            sell_transaction_id = (
                event.get("Transaction ID")
            )


            while sell_quantity > 0:


                # -------------------------
                # Check holdings
                # -------------------------

                if not lots[stock]:

                    raise ValueError(

                        f"Not enough {stock} "
                        f"shares to complete SELL."

                    )


                # -------------------------
                # Oldest FIFO lot
                # -------------------------

                oldest_lot = lots[stock][0]


                # -------------------------
                # Match quantity
                # -------------------------

                matched_quantity = min(

                    sell_quantity,

                    oldest_lot["quantity"]

                )


                # -------------------------
                # BUY charge
                # -------------------------

                charge_per_share = float(

                    oldest_lot.get(
                        "charge_per_share",
                        0
                    )

                )


                buy_charge_for_match = (

                    charge_per_share *
                    matched_quantity

                )


                # -------------------------
                # Adjusted BUY price
                # -------------------------

                adjusted_buy_price = (

                    oldest_lot["price"]
                    + charge_per_share

                )


                # -------------------------
                # Raw gross P&L
                # -------------------------

                raw_gross_profit = (

                    sell_price -
                    oldest_lot["price"]

                ) * matched_quantity


                # -------------------------
                # P&L after BUY charges
                # -------------------------

                profit = (

                    sell_price -
                    adjusted_buy_price

                ) * matched_quantity


                realised_profit += profit


                # -------------------------
                # Save FIFO match
                # -------------------------

                matches.append({

                    "Stock":
                        stock,

                    "Buy Price":
                        oldest_lot["price"],

                    "Adjusted Buy Price":
                        adjusted_buy_price,

                    "Sell Price":
                        sell_price,

                    "Quantity":
                        matched_quantity,

                    "Raw Gross P&L":
                        raw_gross_profit,

                    "Buy Charges":
                        buy_charge_for_match,

                    "Gross P&L":
                        profit,

                    "Buy Transaction ID":
                        oldest_lot.get(
                            "Transaction ID"
                        ),

                    "Sell Transaction ID":
                        sell_transaction_id

                })


                # -------------------------
                # Reduce FIFO lot
                # -------------------------

                oldest_lot["quantity"] -= (
                    matched_quantity
                )


                sell_quantity -= (
                    matched_quantity
                )


                # Remove empty lot
                if oldest_lot["quantity"] == 0:

                    lots[stock].popleft()


        # =================================
        # STOCK SPLIT
        # =================================

        elif event_type == "SPLIT":

            old_lots = [

                dict(lot)

                for lot in lots[stock]

            ]


            adjusted_lots = apply_split_to_lots(

                old_lots,

                old_shares=int(
                    event["Old Shares"]
                ),

                new_shares=int(
                    event["New Shares"]
                )

            )


            # Preserve charge information
            for old_lot, new_lot in zip(
                old_lots,
                adjusted_lots
            ):

                if "buy_charge" in old_lot:

                    new_lot["buy_charge"] = (
                        old_lot["buy_charge"]
                    )


                if "quantity" in new_lot:

                    new_quantity = float(
                        new_lot["quantity"]
                    )

                    new_lot[
                        "charge_per_share"
                    ] = (

                        old_lot.get(
                            "buy_charge",
                            0
                        ) / new_quantity

                        if new_quantity > 0

                        else 0

                    )


                new_lot[
                    "Transaction ID"
                ] = old_lot.get(
                    "Transaction ID"
                )


            lots[stock] = deque(
                adjusted_lots
            )


        # =================================
        # BONUS
        # =================================

        elif event_type == "BONUS":

            old_lots = [

                dict(lot)

                for lot in lots[stock]

            ]


            adjusted_lots = apply_bonus_to_lots(

                old_lots,

                bonus_for=int(
                    event["Bonus For"]
                ),

                bonus_receive=int(
                    event["Bonus Receive"]
                )

            )


            # Preserve transaction information
            # and redistribute existing charges
            for old_lot, new_lot in zip(
                old_lots,
                adjusted_lots
            ):

                new_lot[
                    "buy_charge"
                ] = old_lot.get(
                    "buy_charge",
                    0
                )


                new_quantity = float(
                    new_lot["quantity"]
                )


                new_lot[
                    "charge_per_share"
                ] = (

                    new_lot["buy_charge"]
                    / new_quantity

                    if new_quantity > 0

                    else 0

                )


                new_lot[
                    "Transaction ID"
                ] = old_lot.get(
                    "Transaction ID"
                )


            lots[stock] = deque(
                adjusted_lots
            )


        # =================================
        # UNKNOWN EVENT
        # =================================

        else:

            raise ValueError(

                f"Unknown event type: "
                f"{event_type}"

            )


    # =====================================
    # RETURN
    # =====================================

    return (

        realised_profit,

        lots,

        matches

    )