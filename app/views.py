from app import app
import os
import socket
import json
import urllib2
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
		TestExport(ServerAddress)
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


def TestDef(uid, server):
    returnText = "test server " + server + " with id " + uid
    return returnText

def TestExport(server):
	novus_export = open('app/files/test.csv', 'w+')
	novus_export.write(server)
	novus_export.close
