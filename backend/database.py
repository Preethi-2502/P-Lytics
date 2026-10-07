import sqlite3
from pathlib import Path


# -----------------------------
# DATABASE LOCATION
# -----------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATABASE_FOLDER = PROJECT_FOLDER / "database"

DATABASE_FOLDER.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_FOLDER / "portfolio.db"


# -----------------------------
# CONNECT TO DATABASE
# -----------------------------

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


# -----------------------------
# CREATE TABLES
# -----------------------------

def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_date TEXT NOT NULL,
            stock TEXT NOT NULL,
            trade_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS charges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER,
            brokerage REAL DEFAULT 0,
            stt REAL DEFAULT 0,
            other_charges REAL DEFAULT 0,
            FOREIGN KEY (transaction_id)
                REFERENCES transactions(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS corporate_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_date TEXT NOT NULL,
            stock TEXT NOT NULL,
            action_type TEXT NOT NULL,
            ratio_old INTEGER,
            ratio_new INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS charge_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock TEXT NOT NULL,
            trade_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            brokerage REAL DEFAULT 0,
            stt REAL DEFAULT 0,
            exchange_charges REAL DEFAULT 0,
            gst REAL DEFAULT 0,
            other_charges REAL DEFAULT 0,
            total_charges REAL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


# -----------------------------
# INSERT ONE TRANSACTION
# -----------------------------

def insert_transaction(
    trade_date,
    stock,
    trade_type,
    quantity,
    price
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (trade_date, stock, trade_type, quantity, price)
        VALUES (?, ?, ?, ?, ?)
    """, (
        str(trade_date),
        stock,
        trade_type,
        int(quantity),
        float(price)
    ))

    connection.commit()
    connection.close()


# -----------------------------
# INSERT MULTIPLE TRANSACTIONS
# -----------------------------

def insert_transactions(transactions):

    # IMPORTANT:
    # If transactions is a Pandas DataFrame,
    # convert it to a list of dictionaries.

    if hasattr(transactions, "to_dict"):
        transactions = transactions.to_dict("records")

    connection = get_connection()
    cursor = connection.cursor()

    for trade in transactions:

        cursor.execute("""
            INSERT INTO transactions
            (trade_date, stock, trade_type, quantity, price)
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(trade["Date"]),
            trade["Stock"],
            trade["Type"],
            int(trade["Quantity"]),
            float(trade["Price"])
        ))

    connection.commit()
    connection.close()


# -----------------------------
# CLEAR TRANSACTIONS
# -----------------------------

def clear_transactions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM transactions")

    connection.commit()
    connection.close()
def get_transactions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT trade_date, stock, trade_type, quantity, price
        FROM transactions
        ORDER BY trade_date
    """)

    rows = cursor.fetchall()

    connection.close()

    transactions = []

    for row in rows:

        transactions.append({
            "Date": row[0],
            "Stock": row[1],
            "Type": row[2],
            "Quantity": row[3],
            "Price": row[4]
        })

    return transactions

# -----------------------------
# TEST DATABASE
# -----------------------------
def get_all_transactions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, trade_date, stock, trade_type, quantity, price
        FROM transactions
        ORDER BY trade_date, id
    """)

    rows = cursor.fetchall()

    connection.close()

    transactions = []

    for row in rows:

        transactions.append({
            "id": row[0],
            "Date": row[1],
            "Stock": row[2],
            "Type": row[3],
            "Quantity": row[4],
            "Price": row[5]
        })

    return transactions
def insert_charge_records(charges):

    if hasattr(charges, "to_dict"):
        charges = charges.to_dict("records")

    connection = get_connection()
    cursor = connection.cursor()

    # Get transactions in database order
    cursor.execute("""
        SELECT
            id,
            stock,
            trade_type,
            quantity
        FROM transactions
        ORDER BY id
    """)

    transactions = cursor.fetchall()

    print("\nTransactions available for charge matching:")
    print(transactions)

    # Keep track of transactions already used
    used_ids = set()

    for charge in charges:

        charge_stock = str(
            charge["Stock"]
        ).strip().upper()

        charge_type = str(
            charge["Type"]
        ).strip().upper()

        charge_quantity = int(
            charge["Quantity"]
        )

        transaction_id = None

        # Find matching transaction
        for row in transactions:

            row_id = row[0]
            row_stock = str(row[1]).strip().upper()
            row_type = str(row[2]).strip().upper()
            row_quantity = int(row[3])

            if row_id in used_ids:
                continue

            if (
                row_stock == charge_stock
                and row_type == charge_type
                and row_quantity == charge_quantity
            ):

                transaction_id = row_id
                used_ids.add(row_id)

                break

        print(
            "Matching charge:",
            charge_stock,
            charge_type,
            charge_quantity,
            "→ Transaction ID:",
            transaction_id
        )

        cursor.execute("""
            INSERT INTO charge_records
            (
                stock,
                trade_type,
                quantity,
                brokerage,
                stt,
                exchange_charges,
                gst,
                other_charges,
                total_charges,
                transaction_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            charge_stock,
            charge_type,
            charge_quantity,

            float(charge["Brokerage"]),
            float(charge["STT"]),
            float(charge["Exchange Charges"]),
            float(charge["GST"]),
            float(charge["Other Charges"]),
            float(charge["Total Charges"]),

            transaction_id

        ))

    connection.commit()
    connection.close()

    print(
        "Charge records inserted successfully."
    )
def get_charge_records():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            stock,
            trade_type,
            quantity,
            brokerage,
            stt,
            exchange_charges,
            gst,
            other_charges,
            total_charges,
            transaction_id
        FROM charge_records
        ORDER BY id
    """)

    rows = cursor.fetchall()

    connection.close()

    charges = []

    for row in rows:

        charges.append({

            "id": row[0],

            "Stock": row[1],

            "Type": row[2],

            "Quantity": row[3],

            "Brokerage": row[4],

            "STT": row[5],

            "Exchange Charges": row[6],

            "GST": row[7],

            "Other Charges": row[8],

            "Total Charges": row[9],

            "Transaction ID": row[10]

        })

    return charges

def clear_charge_records():

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM charge_records")

        connection.commit()
        connection.close()

        def insert_corporate_action(
                action_date,
                stock,
                action_type,
                ratio_old,
                ratio_new
        ):
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO corporate_actions
                (
                    action_date,
                    stock,
                    action_type,
                    ratio_old,
                    ratio_new
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                str(action_date),
                stock,
                action_type,
                int(ratio_old),
                int(ratio_new)
            ))

            connection.commit()
            connection.close()
def insert_corporate_action(
    action_date,
    stock,
    action_type,
    ratio_old,
    ratio_new
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO corporate_actions
        (
            action_date,
            stock,
            action_type,
            ratio_old,
            ratio_new
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        str(action_date),
        stock,
        action_type,
        int(ratio_old),
        int(ratio_new)
    ))

    connection.commit()
    connection.close()
def get_corporate_actions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            action_date,
            stock,
            action_type,
            ratio_old,
            ratio_new
        FROM corporate_actions
        ORDER BY action_date, id
    """)

    rows = cursor.fetchall()

    connection.close()

    actions = []

    for row in rows:

        actions.append({
            "id": row[0],
            "Date": row[1],
            "Stock": row[2],
            "Type": row[3],
            "Old Shares": row[4],
            "New Shares": row[5]
        })

    return actions
def clear_corporate_actions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM corporate_actions")

    connection.commit()
    connection.close()
def add_transaction_id_to_charge_records():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(charge_records)")

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "transaction_id" not in columns:

        cursor.execute("""
            ALTER TABLE charge_records
            ADD COLUMN transaction_id INTEGER
        """)
        add_transaction_id_to_charge_records()
        connection.commit()

    connection.close()
if __name__ == "__main__":

    create_tables()

    print("Database created successfully!")
    print("Database location:")
    print(DATABASE_PATH)