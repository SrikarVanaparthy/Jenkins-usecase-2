import sys
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import pyodbc
import os

# ---- CONFIG ----
BASE_DIR = os.path.dirname(__file__)
CSV_FILE_PATH = os.path.join(BASE_DIR, '..', 'data', 'sample.csv')
ROW_COUNT_FILE = os.path.join(BASE_DIR, '..', 'row_count.txt')

DB_CONFIG = {
    'server': '34.170.77.150',
    'database': 'testdb',
    'username': 'sqlserver',
    'password': 'P@ssword@123',
    'driver': '{ODBC Driver 18 for SQL Server}',
    'port': 1433
}

TABLE_NAME = 'people'

def get_connection():
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']},{DB_CONFIG['port']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

def get_existing_ids(cursor):
    # Get the existing ids in the database
    cursor.execute(f"SELECT id FROM {TABLE_NAME}")
    return {row[0] for row in cursor.fetchall()}

def row_exists_and_different(cursor, row):
    # Check if the row exists by id
    check_query = f"SELECT id, fname, lname FROM {TABLE_NAME} WHERE id = ?"
    cursor.execute(check_query, row['id'])
    result = cursor.fetchone()
    
    if not result:
        return False, True  # Doesn't exist → insert
    # Exists, but we check if fname or lname has changed
    return True, (result[1] != row['fname'] or result[2] != row['lname'])  # Check if fname or lname has changed

def load_data():
    df = pd.read_csv(CSV_FILE_PATH)
    conn = get_connection()
    cursor = conn.cursor()

    # Get pre-insert count and save
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    pre_count = cursor.fetchone()[0]
    with open(ROW_COUNT_FILE, "w") as f:
        f.write(str(pre_count))

    # Get all existing ids in the table
    existing_ids = get_existing_ids(cursor)

    insert_query = f"INSERT INTO {TABLE_NAME} (id, fname, lname) VALUES (?, ?, ?)"
    update_query = f"UPDATE {TABLE_NAME} SET fname = ?, lname = ? WHERE id = ?"
    delete_query = f"DELETE FROM {TABLE_NAME} WHERE id = ?"

    # Set of IDs from the CSV
    csv_ids = set(df['id'])

    # Step 1: Handle deletions (IDs in DB that are not in CSV)
    ids_to_delete = existing_ids - csv_ids
    for id_to_delete in ids_to_delete:
        cursor.execute(delete_query, (id_to_delete,))
        print(f"Deleted row with id {id_to_delete}")

    # Step 2: Insert and Update data
    for _, row in df.iterrows():
        exists, needs_update = row_exists_and_different(cursor, row)
        if not exists:
            # Insert new row
            cursor.execute(insert_query, (row['id'], row['fname'], row['lname']))
            print(f"Inserted row with id {row['id']}")
        elif needs_update:
            # Update the existing row with the id
            cursor.execute(update_query, (row['fname'], row['lname'], row['id']))
            print(f"Updated row with id {row['id']}")

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Data sync complete with insert/update/delete logic.")

if __name__ == "__main__":
    load_data()
