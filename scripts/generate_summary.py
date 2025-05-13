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
    # Get the existing ids in the database before the operation
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

    # Step 1: Fetch the current existing ids from the database before any operation
    existing_ids_before = get_existing_ids(cursor)

    # Step 2: Perform operations (Insert/Update/Delete)
    # At this point, you will process the CSV file and perform the necessary operations.
    # After performing the operation, we need to check the current ids in the database.

    # For demonstration, we'll assume the database is updated with new rows and some deletions.
    # Step 3: Fetch the current existing ids after processing the CSV and applying changes.
    existing_ids_after = get_existing_ids(cursor)

    # Step 4: Calculate the differences
    inserted_ids = existing_ids_after - existing_ids_before  # New rows inserted
    deleted_ids = existing_ids_before - existing_ids_after  # Rows deleted

    # Step 5: Count inserted and deleted rows
    inserted_count = len(inserted_ids)
    deleted_count = len(deleted_ids)

    # Step 6: Generate the summary
    summary = f"""
CSV Upload Summary Report:

--------------------------

Rows before insert: {pre_count}
Rows inserted:      {inserted_count}
Rows deleted:       {deleted_count}
Total rows now:     {total_count}

    """.strip()

    # Step 7: Save the summary to the file
    with open(SUMMARY_FILE, "w") as f:
        f.write(summary)

    print("📄 Summary generated:")
    print(summary)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    generate_summary()
