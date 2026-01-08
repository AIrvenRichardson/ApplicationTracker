# This file is designed to import to the database from a csv, the format is identical to the database in order.
# Only real difference is how dates are formatted, and that will be fixed by this script.

import csv, sqlite3
from datetime import datetime


with open('importScript/test.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    con = sqlite3.connect("applications.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS applications(company text, title text, date text, url text, status text)")

    for row in reader:
        print(row['Employer'], row['Title'], row['Date'], row['Link'], row['Response?'])
        
        date = datetime.strptime(row['Date'], '%m/%d/%Y')
        datestring = date.strftime('%Y-%m-%d')
  
        cur.execute(f"""
                INSERT INTO applications VALUES
                ('{row["Employer"]}', '{row["Title"]}', '{datestring}', '{row["Link"]}', '{row["Response?"]}')
                """)
    
    con.commit()