import sqlite3


def main():
    con = sqlite3.connect("applications.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS applications(company text, title text, date text, url text, status text)")

    cur.execute("""
                INSERT INTO applications VALUES
                ('test', 'swe', '2026-01-05', 'pooptown.org', 'not yet')
                """)
    
    con.commit()

    res = cur.execute("SELECT * FROM applications")
    print(res.fetchall())
    return


main()