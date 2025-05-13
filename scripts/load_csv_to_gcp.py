import pandas as pd

import pyodbc

import os
 
# ---- CONFIG ----

BASE_DIR = os.path.dirname(__file__)

CSV_FILE_PATH = os.path.join(BASE_DIR, '..', 'data', 'sample.csv')

ROW_COUNT_FILE = os.path.join(BASE_DIR, '..', 'row_count.txt')
 
# SQL Server DB config

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
 
def load_data():

    df = pd.read_csv(CSV_FILE_PATH)

    conn = get_connection()

    cursor = conn.cursor()
 
    # Get pre-insert count and save

    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")

    pre_count = cursor.fetchone()[0]
 
    with open(ROW_COUNT_FILE, "w") as f:

        f.write(str(pre_count))
 
    # Insert data

    insert_query = f"INSERT INTO {TABLE_NAME} (fname, lname) VALUES (?, ?)"

    for _, row in df.iterrows():

        cursor.execute(insert_query, (row['fname'], row['lname']))
 
    conn.commit()

    cursor.close()

    conn.close()
 
    print("✅ Data loaded into GCP SQL Server.")
 
if __name__ == "__main__":

    load_data()

 