import pandas as pd
import mysql.connector
import os

# ---- CONFIG ----
BASE_DIR = os.path.dirname(__file__)
CSV_FILE_PATH = os.path.join(BASE_DIR, '..', 'data', 'sample.csv')
ROW_COUNT_FILE = os.path.join(BASE_DIR, '..', 'row_count.txt')

db_config = {
    'host': '34.170.77.150',
    'user': 'sqlserver',
    'password': 'P@ssword@123',
    'database': 'testdb',
    'port': 3306
}

TABLE_NAME = 'people'

# ---- MAIN ----
def load_data():
    df = pd.read_csv(CSV_FILE_PATH)
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get pre-insert count and write to file
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    pre_count = cursor.fetchone()[0]

    with open(ROW_COUNT_FILE, "w") as f:
        f.write(str(pre_count))

    # Insert data
    insert_query = f"INSERT INTO {TABLE_NAME} (id, fname, lname) VALUES (%s, %s, %s)"
    for _, row in df.iterrows():
        cursor.execute(insert_query, (row['id'], row['fname'], row['lname']))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data loaded into GCP MySQL.")

if __name__ == "__main__":
    load_data()
