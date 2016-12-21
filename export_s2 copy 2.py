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

print ("APICommand,EncodedNum1,CardFormat1,FirstName,LastName,Accesslevel1,PersonID,PictureFile,PIN")

for row in rows:
    printStr = 0
    userStr = "AddPerson,"
    fobcur = conn.cursor()
    fobcur.execute("SELECT * from novuskey WHERE ownerid = %s", (row[0],))

    fob = fobcur.fetchall()

    for sub_fob in fob:
        # print sub_fob
        printStr = 1
        if sub_fob != None:
            fob_fc = sub_fob[3].split(":")[1].split("-")[0]
            fob_id = sub_fob[3].split(":")[1].split("-")[1]
        # print "First Name: ", row[3], "\nLast Name: ", row[5], "\nCard FC: ", fob_fc, "\nCard Number: ", fob_id
            userStr = userStr + fob_fc + "," + fob_id + ","
        # accur = conn.cursor()
        # accur.execute("SELECT * from usergroupmember where memberid = %s", (row[0],))
        # ac_group = accur.fetchall()
        # if ac_group != None:
        #     print "Access Levels: "
        #     for level in ac_group:
        #         grp_cur = conn.cursor()
        #         grp_cur.execute("SELECT * from usergroup where id = %s", (level[2],))
        #         grp_name = grp_cur.fetchall()
        #         print "".join('%s'%x for x in grp_name[0][1] )
        #     print "\n"

    userStr = userStr + row[3] + "," #first name
    userStr = userStr + row[5] + ",,,," #last name and padding

    if printStr == 1 and row[3] != None:
        print userStr
