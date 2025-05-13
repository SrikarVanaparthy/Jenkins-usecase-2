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
 
    # Get current row count

    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")

    total_count = cursor.fetchone()[0]
 
    inserted_count = total_count - pre_count
 
    summary = f"""

CSV Upload Summary Report:

--------------------------

Rows before insert: {pre_count}

Rows inserted:      {inserted_count}

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

 