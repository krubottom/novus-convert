from app import app
import psycopg2
import os
import socket
import json
import urllib2
import time
from flask import render_template, flash, redirect, url_for, abort, send_file, request
from werkzeug import secure_filename
from .forms import PageForm


# Return a generic static HTML page as base page
@app.route("/")
def Main():
	return render_template('index.html', title='Home', links=site_map_links())

# Show directory of files for download
# Removing AutoIndex, still needs lots of fixes
@app.route('/files/', defaults={'req_path': ''})
@app.route('/files/<path:req_path>')
@app.route('/files')
def Files(req_path):
    BASE_DIR = 'app/files'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
		# return "req_path: " + req_path + "<br><br>abs_path: " + abs_path
		return send_file('files/' + req_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files, links=site_map_links())

# Form to convert
@app.route("/convert", methods = ['GET', 'POST'])
def Convert():
	form = PageForm()
	if form.validate_on_submit():
		ServerAddress = form.ServerAddress.data
		uid = form.uid.data
		SiteName = form.SiteName.data
		TestExport(ServerAddress,uid,SiteName)
		return render_template('formreturn.html', title='Novus Return', textfield=TestDef(uid,ServerAddress), links=site_map_links())
	return render_template('formentry.html', title='Details Entry', form=form, links=site_map_links())

def site_map_links():
	links = []
	for rule in app.url_map.iter_rules():
		# Filter out rules we can't navigate to in a browser
		# and rules that require parameters
		if "GET" in rule.methods and len(rule.arguments)==0:
			url = url_for(rule.endpoint, **(rule.defaults or {}))
			links.append((url, rule.endpoint))
	return links

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

def TestDef(uid, server):
    returnText = "test server " + server + " with id " + uid
    return returnText

def TestExport(server,uid,sitename):
	conn = psycopg2.connect("dbname='novus6' user='root' host='" + server + "' password='novus' port='5432'")
	cur = conn.cursor()
	cur.execute("""SELECT * from person""")
	rows = cur.fetchall()
	novus_export = open('app/files/' + sitename + "-" + time.strftime("%Y%m%d-%H%M%S") + '.csv', 'w+')
	novus_export.write("COMMAND,FIRSTNAME,LASTNAME,CREDENTIALS,NOTES,ACCESSLEVELS,PersonID\n")
	for row in rows:
		strHasFob = False
		strCommand = "AddPerson,"

		strFirstName = row[3].replace(',', '') + ","
		strLastName = row[5].replace(',', '') + ","

		if row[2] == 1:
			strLocked = "Active"
		else:
			strLocked = "Disabled"

		strCredentials = "{"

		fobcur = conn.cursor()
		fobcur.execute("SELECT * from novuskey WHERE ownerid = %s", (row[0],))
		fob = fobcur.fetchall()
		for sub_fob in fob:
			if sub_fob[3].startswith("wg26") and sub_fob != None:
				fob_fc = sub_fob[3].split(":")[1].split("-")[0]
				fob_id = sub_fob[3].split(":")[1].split("-")[1]
				strCredentials = strCredentials + fob_id + "~" + fob_id + "~FC " + fob_fc + "~Active~~|"
				strHasFob = True
		strCredentials = strCredentials[:-1] + "}"

		strAccessLevel = ""

		if row[7] != None:
			strAutoDisble = row[7].strftime("%Y-%m-%d")
		else:
			strAutoDisble = ""

		if strHasFob:
			novus_export.write(strFirstName + strLastName + strCredentials + "notes,accesslevel,id\n")
	novus_export.close
