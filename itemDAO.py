#!/usr/bin/env python3

import psycopg2

con = psycopg2.connect(database="whatsin_db", user="postgres", password="johnsmells7", host="whatsin-db.cubhsslyixfb.eu-west-2.rds.amazonaws.com", port="5432")


curr = con.cursor()
curr.execute("SELECT * FROM fridge")
rows = curr.fetchall()

#for row in rows:
#    print("id = ", row[0])
 #   print("item_name = ", row[1])
  #  print("quantity = ", row[2])
   # print("use_by = ", row[3])

for row in rows:
    print(row)

print("Operation complete, goodnight!")

con.close()
