import psycopg2
import sys

# make this be a real check, breakup into def

try:
    conn = psycopg2.connect("dbname='novus6' user='root' host='172.16.171.131' password='novus' port='5432'")
except:
    e = sys.exc_info()[1]
    print e

cur = conn.cursor()
cur.execute("""SELECT * from person""")
rows = cur.fetchall()

# need to add PIN
print ("COMMAND,LASTNAME,FIRSTNAME,CREDENTIALS,ACCESSLEVELS,PIN")

for row in rows:
    printStr = 0
    strCommand = "AddPerson,"
    # Strip out commas in names
    strFirstName = row[3].replace(',', '') + ","
    # Strip out commas in names
    strLastName = row[5].replace(',', '') + ","
    # current account in Novus is locked
    strLocked = row[2]
    strCredentials = "{"
    strAccessLevel = "{"
    strPIN = "{"

    fobcur = conn.cursor()
    fobcur.execute("SELECT * from novuskey WHERE ownerid = %s", (row[0],))

    fob = fobcur.fetchall()
    i = 0
    for sub_fob in fob:
        # print sub_fob[3].startswith("wg26")
        if not sub_fob[3].startswith("wg26") and sub_fob != None:
            strPIN = sub_fob
            printStr = 1
            # print "PIN" + strPIN

        if sub_fob[3].startswith("wg26") and sub_fob != None:
            fob_fc = sub_fob[3].split(":")[1].split("-")[0]
            fob_id = sub_fob[3].split(":")[1].split("-")[1]
            strCredentials = strCredentials + fob_id + "~" + fob_id + "~FC " + fob_fc + "~Active~~|"
            printStr = 1
            # print "Cred: " + strCredentials

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
    strCredentials = strCredentials[:-1] + "}"
    # A user can only have one PIN
    # if strPIN.endswith("|"):
    #     strPIN = strPIN[:-1] + "}"
    # else:
    #     strPIN = ""

    if printStr == 1:
        print strCommand + strFirstName + strLastName + strCredentials + "," + strAccessLevel + "," + strPIN

# Make calls functions

# Need to get the server address and userID
# return a list of Credentials, not the string it currently does
def GetCredentials(uid, server):
    strCredentials = ""
    conn = psycopg2.connect("dbname='novus6' user='root' host=%s password='novus' port='5432'", server)
    fobcur = conn.cursor()
    fobcur.execute("SELECT * from novuskey WHERE ownerid = %s", uid)
    for sub_fob in fob:
        if sub_fob[3].startswith("wg26") and sub_fob != None:
            fob_fc = sub_fob[3].split(":")[1].split("-")[0]
            fob_id = sub_fob[3].split(":")[1].split("-")[1]
            strCredentials = strCredentials + fob_id + "~" + fob_id + "~FC " + fob_fc + "~Active~~|"
            # print "Cred: " + strCredentials
    return strCredentials

# Need to get the server anddress and userID
# Return a number
def GetPINs(uid, server):
    strPIN = ""
    conn = psycopg2.connect("dbname='novus6' user='root' host=%s password='novus' port='5432'", server)
    fobcur = conn.cursor()
    fobcur.execute("SELECT * from novuskey WHERE ownerid = %s", uid)
    for sub_fob in fob:
        if not sub_fob[3].startswith("wg26") and sub_fob != None:
            strPIN = sub_fob
    return strPIN

def GetAccessLevels(id, server):
    accur = conn.cursor()
    accur.execute("SELECT * from usergroupmember where memberid = %s", user)
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
    return strAccessLevel
