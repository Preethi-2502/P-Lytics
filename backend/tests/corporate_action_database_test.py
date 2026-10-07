from database import (
    create_tables,
    clear_corporate_actions,
    insert_corporate_action,
    get_corporate_actions
)


# Create tables
create_tables()


# Remove previous test data
clear_corporate_actions()


# Insert a stock split
insert_corporate_action(
    action_date="2026-09-05",
    stock="ALPHA",
    action_type="SPLIT",
    ratio_old=1,
    ratio_new=2
)


# Read it back
actions = get_corporate_actions()


print("\nCorporate Actions from Database")
print("--------------------------------")

for action in actions:

    print(action)