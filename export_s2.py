import psycopg2
import sys

try:
    conn = psycopg2.connect("dbname='novus6' user='root' host='172.16.171.128' password='novus' port='5432'")
except:
    e = sys.exc_info()[1]
    print e

cur = conn.cursor()
cur.execute("""SELECT * from person""")
rows = cur.fetchall()

for row in rows:
    fobcur = conn.cursor()
    fobcur.execute("SELECT * from novuskey WHERE id = %s", (row[0],))
    fob = fobcur.fetchone()
    fob_fc = fob[3].split(":")[1].split("-")[0]
    fob_id = fob[3].split(":")[1].split("-")[1]
    print "First Name: ", row[3], "\nLast Name: ", row[5], "\nCard FC: ", fob_fc, "\nCard Number: ", fob_id, "\n\n"
