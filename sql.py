import sqlite3


def fetch_output(db, sql="select * from user_details"):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()

    for row in rows:
        print(row)

    return rows
