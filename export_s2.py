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

print ("COMMAND,LASTNAME,FIRSTNAME,CREDENTIALS,ACCESSLEVELS")

for row in rows:
    printStr = 0
    strCommand = "AddPerson,"
    strFirstName = row[3].replace(',', '') + ","
    strLastName = row[5].replace(',', '') + ","
    strCredentials = ""
    strAccessLevel = "{"

    fobcur = conn.cursor()
    fobcur.execute("SELECT * from novuskey WHERE ownerid = %s", (row[0],))

    fob = fobcur.fetchall()
    i = 0
    for sub_fob in fob:
        i = i +1
        if i == 1:
            strCredentials = "{"
        # need to add error checking for PIN vs KeyCard
        printStr = 1
        if sub_fob != None:
            fob_fc = sub_fob[3].split(":")[1].split("-")[0]
            fob_id = sub_fob[3].split(":")[1].split("-")[1]
            strCredentials = strCredentials + fob_id + "~" + fob_id + "~FC " + fob_fc + "~Active~~"
        if len(fob) > i:
            strCredentials = strCredentials + "|"
        if i == len(fob):
            strCredentials = strCredentials + "}"

        accur = conn.cursor()
        accur.execute("SELECT * from usergroupmember where memberid = %s", (row[0],))
        ac_group = accur.fetchall()
        if ac_group != None:
            # Access Levels
            for level in ac_group:
                grp_cur = conn.cursor()
                grp_cur.execute("SELECT * from usergroup where id = %s", (level[2],))
                grp_name = grp_cur.fetchall()
                ai = 0
                for ac_level in grp_name:
                    ai == ai + 1
                    strAccessLevel = strAccessLevel + ac_level[1]
                    if len(ac_level) > ai:
                        strAccessLevel = strAccessLevel + "|"
                # print "".join('%s'%x for x in grp_name[0][1] )
    strAccessLevel = strAccessLevel[:-1] + "}"
    if printStr == 1:
        print strCommand + strFirstName + strLastName + strCredentials + "," + strAccessLevel
