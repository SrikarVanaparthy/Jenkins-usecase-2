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

def row_exists_and_different(cursor, row):
    check_query = f"SELECT fname, lname FROM {TABLE_NAME} WHERE id = ?"
    cursor.execute(check_query, row['id'])
    result = cursor.fetchone()
    if not result:
        return False, True  # Doesn't exist → insert
    return True, (result[0] != row['fname'] or result[1] != row['lname'])  # Exists, but different → update

def load_data():
    df = pd.read_csv(CSV_FILE_PATH)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    pre_count = cursor.fetchone()[0]
    with open(ROW_COUNT_FILE, "w") as f:
        f.write(str(pre_count))

    insert_query = f"INSERT INTO {TABLE_NAME} (id, fname, lname) VALUES (?, ?, ?)"
    update_query = f"UPDATE {TABLE_NAME} SET fname = ?, lname = ? WHERE id = ?"

    for _, row in df.iterrows():
        exists, needs_update = row_exists_and_different(cursor, row)
        if not exists:
            cursor.execute(insert_query, (row['id'], row['fname'], row['lname']))
        elif needs_update:
            cursor.execute(update_query, (row['fname'], row['lname'], row['id']))
        # else: no need to do anything

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Data sync complete with insert/update logic.")

if __name__ == "__main__":
    load_data()
