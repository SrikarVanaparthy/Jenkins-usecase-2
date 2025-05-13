import sys
sys.stdout.reconfigure(encoding='utf-8')

import pyodbc
import os

# ---- CONFIG ----

BASE_DIR = os.path.dirname(__file__)

SUMMARY_FILE = os.path.join(BASE_DIR, '..', 'upload_summary.txt')

ROW_COUNT_FILE = os.path.join(BASE_DIR, '..', 'row_count.txt')

db_config = {

    'server': '34.170.77.150',

    'user': 'sqlserver',

    'password': 'P@ssword@123',

    'database': 'testdb',

    'port': 1433,

    'driver': '{ODBC Driver 18 for SQL Server}'

}

TABLE_NAME = 'people'

def get_connection():

    conn_str = (

        f"DRIVER={db_config['driver']};"

        f"SERVER={db_config['server']},{db_config['port']};"

        f"DATABASE={db_config['database']};"

        f"UID={db_config['user']};"

        f"PWD={db_config['password']};"

        "TrustServerCertificate=yes;"

    )

    return pyodbc.connect(conn_str)

def get_existing_ids(cursor):
    # Get the existing ids in the database
    cursor.execute(f"SELECT id FROM {TABLE_NAME}")
    return {row[0] for row in cursor.fetchall()}

# ---- MAIN ----

def generate_summary():
    # Read previous row count
    if not os.path.exists(ROW_COUNT_FILE):
        print("⚠️ Previous row count not found.")
        pre_count = 0
    else:
        with open(ROW_COUNT_FILE, "r") as f:
            pre_count = int(f.read().strip())

    conn = get_connection()
    cursor = conn.cursor()

    # Get current row count and existing ids in the table
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    total_count = cursor.fetchone()[0]

    existing_ids_before = get_existing_ids(cursor)

    # Step 1: Insert, Update, and Delete rows logic would go here
    # We'll assume that you have performed the necessary operations (insert/update/delete)
    # and now you want to track how many rows have been deleted, inserted, and updated.

    # In this example, we'll assume you have a CSV and data has been processed.
    # After processing the CSV, you should compare the `existing_ids_before` with the current `existing_ids_after`.

    # Step 2: Simulate operations (replace this with actual insert/update/delete operations)
    existing_ids_after = existing_ids_before  # This should be updated with the new ids after operation
    inserted_ids = existing_ids_after - existing_ids_before  # New rows inserted
    deleted_ids = existing_ids_before - existing_ids_after  # Rows deleted

    # Calculate inserted and deleted rows
    inserted_count = len(inserted_ids)
    deleted_count = len(deleted_ids)

    summary = f"""
CSV Upload Summary Report:

--------------------------

Rows before insert: {pre_count}
Rows inserted:      {inserted_count}
Rows deleted:       {deleted_count}
Total rows now:     {total_count}

    """.strip()

    with open(SUMMARY_FILE, "w") as f:
        f.write(summary)

    print("📄 Summary generated:")
    print(summary)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    generate_summary()
