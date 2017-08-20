import sqlite3
import time
import sys


DB_NAME = "GDELT_dl_logs.sqlite3"
def create_log_DB():
    """Creates the log DB to track which GDELT files have been processed"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE FILES (
    URL TEXT,
    DLTIME TEXT);
    """
    )

    conn.commit()
    conn.close()

def log_file(file_url):
    """Inserts a file into the DB to record it was logged."""
    now = time.time()

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("INSERT INTO FILES VALUES (?, ?)", [file_url, str(now)])
    resp = cur.fetchall()
    print("Insert response is: ")
    print(resp)

    conn.commit()
    conn.close()

def check_file_downloaded(file_url):
    """Checks If the file has already been downloaded."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    SELECT COUNT(*) FROM FILES
    WHERE URL = '{}';
    """.format(file_url))
    count = cur.fetchone()

    try:
        if count[0] == 1:
            return True
        else:
            return False
    except:
        sys.stdout.write("here's were the integer failure was\n")


    cur.close()
    conn.close()

if __name__ == "__main__":
    import subprocess

    create_log_DB()
    print(check_file_downloaded("ABC"))
    print(check_file_downloaded("DEF"))
    subprocess.call(["rm", DB_NAME])
