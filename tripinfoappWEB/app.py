#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 22:18:53 2020

@author: ratan
"""
import trip_classes as tp
from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
import requests 
import datetime
import time
import os, webbrowser, sys
#import yaml
from os import environ
from dotenv import load_dotenv
#load_dotenv()

from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Fetching the current directory path
fileDir = os.path.abspath(os.getcwd())

# Getting the link to credentials file containing keys for Yelp, hikingproject and eventful APIs
#path_keys_yaml = fileDir + "/credentials.yml"
#path_keys_yaml = fileDir + "/../keys/credentials_template.yml"

#with open(path_keys_yaml,'r') as file:
#	keys_list = yaml.load(file, Loader=yaml.FullLoader)

ykey = os.getenv('YKEY') 
hkey = os.getenv('HKEY')
ekey = os.getenv('EKEY')

gyobj = tp.yelp(ykey)
ghobj = tp.hikeproject(hid=hkey,loc='san jose ca usa')
geobj = tp.eventful(ekey)

app = Flask(__name__)

in_params = {'rest_catg':"",'loc':'san jose ca usa','dat':"",'tm':"",'kwords':"",'utm':1594173600}

@app.route("/yelpsortbyrating", methods=['GET', 'POST'])
def yelpsortbyrating():
	global gyobj
	global ghobj 
	global geobj
	gyobj.sort_restsList_rating()
	return render_template('trip_format.html',rests=gyobj.restsList,hikes=ghobj.hikesiteList,events=geobj.eventsList)

@app.route("/yelpsortbyreviews", methods=['GET', 'POST'])
def yelpsortbyreviews():
	global gyobj
	global ghobj 
	global geobj
	gyobj.sort_restsList_numreviews()
	return render_template('trip_format.html',rests=gyobj.restsList,hikes=ghobj.hikesiteList,events=geobj.eventsList)

@app.route("/yelpsortbydistance", methods=['GET', 'POST'])
def yelpsortbydistance():
	global gyobj
	global ghobj 
	global geobj
	gyobj.sort_restsList_distance
	return render_template('trip_format.html',rests=gyobj.restsList,hikes=ghobj.hikesiteList,events=geobj.eventsList)

@app.route("/hikesortbystarvotes", methods=['GET', 'POST'])
def hikesortbystarvotes():
	global gyobj
	global ghobj 
	global geobj
	ghobj.sort_hikesiteList_starvotes()
	return render_template('trip_format.html',rests=gyobj.restsList,hikes=ghobj.hikesiteList,events=geobj.eventsList)

@app.route("/hikesortbystars", methods=['GET', 'POST'])
def hikesortbystars():
	global gyobj
	global ghobj 
	global geobj
	ghobj.sort_restsList_stars()
	return render_template('trip_format.html',rests=gyobj.restsList,hikes=ghobj.hikesiteList,events=geobj.eventsList)

@app.route("/hikesortbylength", methods=['GET', 'POST'])
def hikesortbylength():
	global gyobj
	global ghobj 
	global geobj
	ghobj.sort_restsList_length()
	return render_template('trip_format.html',rests=gyobj.restsList,hikes=ghobj.hikesiteList,events=geobj.eventsList)

@app.route("/eventfulsortbycity", methods=['GET', 'POST'])
def eventfulsortbystarvotes():
	global gyobj
	global ghobj 
	global geobj
	geobj.sort_eventsList_city()
	return render_template('trip_format.html',rests=gyobj.restsList,hikes=ghobj.hikesiteList,events=geobj.eventsList)

@app.route("/eventfulsortbycomments", methods=['GET', 'POST'])
def eventfulsortbystars():
	global gyobj
	global ghobj 
	global geobj
	geobj.sort_eventsList_numcomments()
	return render_template('trip_format.html',rests=gyobj.restsList,hikes=ghobj.hikesiteList,events=geobj.eventsList)

@app.route("/eventfulsortbystarttime", methods=['GET', 'POST'])
def eventfulsortbylength():
	global gyobj
	global ghobj 
	global geobj
	geobj.sort_eventsList_startime()
	return render_template('trip_format.html',rests=gyobj.restsList,hikes=ghobj.hikesiteList,events=geobj.eventsList)


out_params = {}
@app.route("/", methods=['GET', 'POST'])
def home():
	global gyobj
	global ghobj 
	global geobj

	pst=False
	if request.method == 'POST':
		pst=True
		rest_catg = request.form.get('rest_catg')
		loc = request.form.get('loc')
		dat = request.form.get('dat')
		tm = request.form.get('tm')
		kwords = request.form.get('kwords')
		in_params['rest_catg'] = rest_catg
		in_params['loc'] = loc
		in_params['dat'] = dat
		in_params['tm'] = tm
		in_params['kwords'] = kwords
		#utime = int(get_unix_time(in_params['date'],in_params['time']))
		dspl = str(dat).split("/")
		uyr = int(dspl[0])
		umth = int(dspl[1])
		uday = int(dspl[2])
		tspl = str(tm).split(":")
		uhr = int(tspl[0])
		umin = int(tspl[1])
		dt = datetime.datetime(uyr,umth,uday,uhr,umin)
		utm = int(time.mktime(dt.timetuple()))
		in_params['utm'] = utm
		
	yobj = tp.yelp(ykey)
	yobj.set_business_params(search_term=in_params['rest_catg'],loc=in_params['loc'],op_at=in_params['utm'])
	yobj.set_all_business_det()
	gyobj = yobj
	rests_list = yobj.restsList

	hobj = tp.hikeproject(hid=hkey,loc=str(in_params['loc']))
	test_loc = hobj.set_lat_long()
	if test_loc==1:
		hobj.set_hike_params()
	ghobj = hobj
	hike_list = hobj.hikesiteList

	eobj = tp.eventful(ekey)
	eobj.set_event_params(kwds=str(in_params['kwords']),loc=str(in_params['loc']),edate=str(in_params['dat']))
	geobj = eobj
	events_list = eobj.eventsList

	return render_template('trip_format.html',rests=rests_list,hikes=hike_list,events=events_list)

if __name__ == "__main__":
	app.run()
