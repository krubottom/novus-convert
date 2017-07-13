import psycopg2
import sys

# make this be a real check, breakup into def

try:
    conn = psycopg2.connect("dbname='novus6' user='root' host='192.168.118.205' password='novus' port='5432'")
except:
    e = sys.exc_info()[1]
    print e

cur = conn.cursor()
cur.execute("""SELECT * from person""")
rows = cur.fetchall()

# need to add PIN
print ("COMMAND,LASTNAME,FIRSTNAME,CREDENTIALS,ACCESSLEVELS")

for row in rows:
    printStr = 0
    strCommand = "AddPerson,"
    # Strip out commas in names
    strFirstName = row[2].replace(',', '') + ","
    # Strip out commas in names
    strLastName = row[4].replace(',', '') + ","
    # current account in Novus is locked
    strLocked = row[2]
    strCredentials = "{"
    strAccessLevel = "{"
    strPIN = "{"

    # print row[3]

    fobcur = conn.cursor()
    fobcur.execute("SELECT * from novuskey WHERE ownerid = %s", (row[3],))

    fob = fobcur.fetchall()
    i = 0
    for sub_fob in fob:
        # print sub_fob[2]
        # print sub_fob[3].startswith("wg26")
        if not sub_fob[2].startswith("wg26") and sub_fob != None:
            strPIN = sub_fob
            printStr = 1
            # print "PIN" + strPIN

        if sub_fob[2].startswith("wg26") and sub_fob != None:
            fob_fc = sub_fob[2].split(":")[1].split("-")[0]
            fob_id = sub_fob[2].split(":")[1].split("-")[1]
            strCredentials = strCredentials + fob_id + "~" + fob_id + "~AWID FC " + fob_fc + "~Active~~|"
            printStr = 1
            # print "Cred: " + strCredentials

        accur = conn.cursor()
        accur.execute("SELECT * from usergroupmember where memberid = %s", (row[3],))
        # print row[3]
        ac_group = accur.fetchall()
        if ac_group != None:
            # Access Levels
            # print ac_group
            for level in ac_group:
                # print level[0]
                grp_cur = conn.cursor()
                grp_cur.execute("SELECT * from usergroup where id = %s", (level[0],))
                grp_name = grp_cur.fetchall()
                ai = 0
                for ac_level in grp_name:
                    # print "has ac_level"
                    # print ac_level[2]
                    ai == ai + 1
                    if ac_level[2] not in strAccessLevel:
                        strAccessLevel = strAccessLevel + ac_level[2]
                        if len(ac_level) > ai:
                          strAccessLevel = strAccessLevel + "|"

                # print "".join('%s'%x for x in grp_name[0][1] )
    strAccessLevel = strAccessLevel[:-1] + "}"
    strCredentials = strCredentials[:-1] + "}"

    if printStr == 1:
        print strCommand + strFirstName + strLastName + strCredentials + "," + strAccessLevel