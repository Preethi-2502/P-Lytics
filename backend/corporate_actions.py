def apply_bonus(quantity, bonus_for, bonus_receive):
    """
    Calculate the new quantity after a bonus issue.

    Example:
    100 shares
    Bonus ratio = 1:2
    """

    bonus_shares = (quantity // bonus_for) * bonus_receive

    new_quantity = quantity + bonus_shares

    return new_quantity, bonus_shares
def apply_split(quantity, price, old_shares, new_shares):
    """
    Adjust quantity and price after a stock split.

    Example:
    1 old share becomes 2 new shares.
    """

    new_quantity = quantity * new_shares / old_shares
    new_price = price * old_shares / new_shares

    return int(new_quantity), new_price
def apply_bonus_to_lots(lots, bonus_for, bonus_receive):
    """
    Add bonus shares as a separate FIFO lot.

    Example:
    100 shares with a 1:2 bonus
    -> 50 bonus shares
    """

    total_quantity = sum(lot["quantity"] for lot in lots)

    bonus_quantity = (
        total_quantity // bonus_for
    ) * bonus_receive

    if bonus_quantity > 0:

        lots.append({
            "quantity": bonus_quantity,
            "price": 0
        })

    return lots


def apply_split_to_lots(lots, old_shares, new_shares):
    """
    Adjust every FIFO lot after a stock split.
    """

    for lot in lots:

        lot["quantity"] = int(
            lot["quantity"] * new_shares / old_shares
        )

        lot["price"] = (
            lot["price"] * old_shares / new_shares
        )

    return lots
def apply_corporate_action(
    lots,
    action_type,
    bonus_for=1,
    bonus_receive=0,
    old_shares=1,
    new_shares=1
):
    """
    Apply a bonus or split to FIFO lots.

    action_type:
        "BONUS" or "SPLIT"
    """

    if action_type == "BONUS":

        lots = apply_bonus_to_lots(
            lots,
            bonus_for,
            bonus_receive
        )

    elif action_type == "SPLIT":

        lots = apply_split_to_lots(
            lots,
            old_shares,
            new_shares
        )

    else:

        raise ValueError(
            "Unsupported corporate action."
        )

    return lots
if __name__ == "__main__":

    quantity = 100

    # 1 bonus share for every 2 shares
    bonus_for = 2
    bonus_receive = 1

    new_quantity, bonus_shares = apply_bonus(
        quantity,
        bonus_for,
        bonus_receive
    )

    print("Original Quantity:", quantity)
    print("Bonus Shares:", bonus_shares)
    print("New Quantity:", new_quantity)
    if __name__ == "__main__":
        quantity = 100
        price = 200

        # 1 old share becomes 2 new shares
        old_shares = 1
        new_shares = 2

        new_quantity, new_price = apply_split(
            quantity,
            price,
            old_shares,
            new_shares
        )

        print("Original Quantity:", quantity)
        print("Original Price:", price)

        print("New Quantity:", new_quantity)
        print("New Price:", new_price)

        print("Original Value:", quantity * price)
        print("New Value:", new_quantity * new_price)
        if __name__ == "__main__":
            lots = [
                {
                    "quantity": 100,
                    "price": 100
                }
            ]

            print("Before Bonus:")
            print(lots)

            lots = apply_bonus_to_lots(
                lots,
                bonus_for=2,
                bonus_receive=1
            )

            print("\nAfter Bonus:")
            print(lots)
            if __name__ == "__main__":
                lots = [
                    {
                        "quantity": 100,
                        "price": 200
                    }
                ]

                print("Before Split:")
                print(lots)

                lots = apply_split_to_lots(
                    lots,
                    old_shares=1,
                    new_shares=2
                )

                print("\nAfter Split:")
                print(lots)
                if __name__ == "__main__":
                    lots = [
                        {
                            "quantity": 100,
                            "price": 200
                        }
                    ]

                    print("Before Split:")
                    print(lots)

                    lots = apply_corporate_action(
                        lots,
                        action_type="SPLIT",
                        old_shares=1,
                        new_shares=2
                    )

                    print("\nAfter Split:")
                    print(lots)