import sqlite3
from pathlib import Path


# Get the backend folder
project_folder = Path(__file__).resolve().parent.parent

db_path = project_folder / "database" / "portfolio.db"

print("Database path:")
print(db_path)

# Check whether database exists
if not db_path.exists():
    print("ERROR: Database file not found.")
    exit()

# Open database
connection = sqlite3.connect(str(db_path))

cursor = connection.cursor()


# Check existing columns
cursor.execute("PRAGMA table_info(charge_records)")

columns = [
    row[1]
    for row in cursor.fetchall()
]

print("\nExisting columns:")
print(columns)


# Add transaction_id only if needed
if "transaction_id" not in columns:

    cursor.execute("""
        ALTER TABLE charge_records
        ADD COLUMN transaction_id INTEGER
    """)

    connection.commit()

    print("\ntransaction_id added successfully.")

else:

    print("\ntransaction_id already exists.")


connection.close()

print("\nDatabase update complete.")