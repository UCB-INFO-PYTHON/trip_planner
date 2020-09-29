#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:40:17 2020

@author: ratan
"""

import requests
import datetime
import time 
import urllib.request, json
#import tkinter as tk
from geopy.geocoders import Nominatim

import pandas as pd
import numpy as np
from copy import deepcopy

# Defining a global function to get current time 
def get_curr_date_utm():
    dat = datetime.date.today()
    dspl = str(dat).split("-")
    uyr = int(dspl[0])
    umth = int(dspl[1])
    uday = int(dspl[2])
    dt = datetime.datetime(uyr,umth,uday,12,00)
    utm = int(time.mktime(dt.timetuple()))
    return utm

# Defining Restaurant Class to store data type 
class Restaurant: 
    def __init__(self,rest_id):
        self.id = rest_id 
        self.rating = 0
        self.phone = ""
        self.review_count = 0 
        self.url = "" 
        self.address = "" 
        self.city = "" 
        self.state = "" 
        self.zip = ""
        self.price = ""
        self.name = ""
        self.transactions = []
        self.hours = []
        self.catg_alias = []
        self.distance = 0

# Creating class for the Yelp API. Intended to get data related to restaurants for now 
class yelp:
    
    def __init__(self,key= ""):
        self.key = key
        self.restsList = []
    
    # Method to get the business id of all the search results and set various parameters
    def set_business_params(self,search_term='asian food',loc="95123",rad=4000,pr=1,op_at=get_curr_date_utm()): 
        ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
        HEADERS = {'Authorization': 'bearer %s' % self.key}

        PARAMETERS = {'term':search_term, 'location':loc, 'radius':rad, 'price':pr, 'open_at':op_at, 'limit': 10}

        # Make a request 
        response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)

        if response.status_code==200:
            print("Your query to Yelp API for getting business ID data was successful!")
            # convert the JSON strong to a dictionary
            rest_data = response.json()
            if (rest_data['businesses']!=None):
                for rd in rest_data['businesses']:
                    rid = rd['id']
                    rest = Restaurant(rid)
                    rest.rating = rd['rating']
                    rest.price = rd['price']
                    rest.phone = rd['phone']
                    rest.review_count = rd['review_count']
                    rest.url = rd['url']
                    rest.address = rd['location']['address1']
                    rest.city = rd['location']['city']
                    rest.state = rd['location']['state']
                    rest.zip = rd['location']['zip_code']
                    rest.name = rd['name']
                    rest.distance = rd['distance']
                    #print(rest.name,rest.zip,rest.city)
                    if 'pickup' in rd['transactions']: 
                        rest.transactions.append('pickup')
                    if 'delivery' in rd['transactions']:
                        rest.transactions.append('delivery')
                    if 'restaurant_reservation' in rd['transactions']:
                        rest.transactions.append('restaurant_reservation')
                    self.restsList.append(rest)
        else: 
            print("Your query to Yelp API for getting business ID data was not succesful - please try again")
            
            
    # Method to set more details for each of the business returned by Yelp API data query 
    def set_business_det(self,rest):
        
        rid = rest.id
        ENDPOINT = 'https://api.yelp.com/v3/businesses/'+rid
        HEADERS = {'Authorization': 'bearer %s' % self.key}
        PARAMETERS = {'locale':'en_US'}
        
        # Make a request 
        response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)
        
        if response.status_code==200:
            #print("Your query to Yelp API for business details data was successful!")
            rest_det_data = response.json()
            rest.hours= deepcopy(rest_det_data['hours'])
            rest.catg_alias = deepcopy(rest_det_data['categories'])
        else: 
            print("Your query to Yelp API for business details data was not succesful - please try again")
            
    def set_all_business_det(self):
        for rest in self.restsList:
            self.set_business_det(rest)
            
    # Define method to sort restaurants list according to number of reviews
    def sort_restsList_numreviews(self):
        self.restsList.sort(key= lambda x:int(x.review_count), reverse=True)
  
    # Define method to sort restaurants list according to rating
    def sort_restsList_rating(self):
        self.restsList.sort(key= lambda x:float(x.rating), reverse=True)
        return 
        
    # Define method to sort restaurants list according to rating
    def sort_restsList_distance(self):
        self.restsList.sort(key= lambda x:float(x.distance), reverse=True)
        
  
#Creating a class to store the data "hikesite" structure returned from HikeProject
class HikeSite:
    def __init__(self):
        self.name = ""
        self.summary = "" 
        self.difficulty = "" 
        self.stars = 0 
        self.starVotes = 0 
        self.location = ""  
        self.length = 0 
        self.ascent = 0 
        self.descent = 0 
        self.longt = 0
        self.lat = 0 
        self.condstat = "" 
        self.conddet = "" 
        self.conddate = "" 
        
    
# Creating a class 'Hike' for the hikingproject API 
class hikeproject:
    
    def __init__(self,hid,loc):
        self.id = hid
        self.hikesiteList = []
        self.loc = loc
        self.loc_lat = 0
        self.loc_long = 0
        
    # Method to set the ongitude and latitude for the hiking locations 
    def set_lat_long(self): 
        try:
            geolocator = Nominatim(user_agent="trip_planner")
            location = geolocator.geocode(self.loc)
            self.loc_lat = location.latitude
            self.loc_long = location.longitude
            return 1
        except:
            geolocator = Nominatim(user_agent="trip_planner")
            location = geolocator.geocode('san jose ca usa')
            self.loc_lat = location.latitude
            self.loc_long = location.longitude
            return 0

    # Define a function to create all the hike location parameters   
    def set_hike_params(self,max_dist=20):
        ENDPOINT = "https://www.hikingproject.com/data/get-trails"
        PARAMETERS = {'lat':self.loc_lat, 'lon':self.loc_long, 'maxDistance':max_dist, 'key':self.id}
        response = requests.get(ENDPOINT, params=PARAMETERS)

        hikes = response.json()
        if (hikes['trails']!=None):
            for hk in hikes['trails']: 
                hike = HikeSite()
                hike.name = hk['name']
                hike.summary = hk['summary']
                hike.difficulty = hk['difficulty']
                hike.stars = hk['stars']
                hike.starVotes = hk['starVotes']
                hike.location = hk['location']
                hike.length = hk['length']
                hike.ascent = hk['ascent']
                hike.descent = hk['descent']
                hike.longt = hk['longitude']
                hike.lat = hk['latitude']
                hike.condstat = hk['conditionStatus']
                hike.conddet = hk['conditionDetails']
                hike.conddate = hk['conditionDate']
                self.hikesiteList.append(hike)
            
    # Define method to sort restaurants list according to number of reviews
    def sort_hikesiteList_starvotes(self):
        self.hikesiteList.sort(key= lambda x:int(x.starVotes), reverse=True)
  
    # Define method to sort restaurants list according to rating
    def sort_restsList_stars(self):
        self.hikesiteList.sort(key= lambda x:float(x.stars), reverse=True)
        
    # Define method to sort restaurants list according to rating
    def sort_restsList_length(self):
        self.hikesiteList.sort(key= lambda x:float(x.length), reverse=True)
        
       
         
# Creating class to store event returned by Eventful API 
class Event: 
    
    def __init__(self):
        self.venue_name = "" 
        self.start_time = "" 
        self.stop_time = "" 
        self.venue_url = "" 
        self.venue_address = ""
        self.city_name = "" 
        self.lat = "" 
        self.longt = "" 
        self.title = "" 
        self.comment_count = ""
    
# Creating a class for requesting event data from Eventful API 
class eventful:
    

    
    def __init__(self,key=""):
        self.key = key 
        self.eventsList = []
        
    def set_event_params(self,kwds='kids',loc='san jose ca usa',edate='2020/07/12'):
        ENDPOINT = "http://api.eventful.com/json/events/search"
        PARAMETERS = {'keywords':kwds,'location':loc, 'page_size':10, 'within':20, 'unit':'miles', 'date':edate, 'app_key':self.key}
        response = requests.get(ENDPOINT, params=PARAMETERS)
        
        ev = response.json()
        #print(ev['events'])
        if (ev['events']!=None):
            for evt in ev['events']['event']: 
                e = Event() 
                e.venue_name = evt['venue_name']
                e.start_time = evt['start_time']
                e.stop_time = evt['stop_time']
                e.venue_url = evt['venue_url']
                e.venue_address = evt['venue_address']
                e.city_name = evt['city_name']
                e.lat = evt['latitude']
                e.longt = evt['longitude']
                e.title = evt['title']
                e.comment_count = evt['comment_count']
                self.eventsList.append(e)
    
        # Define method to sort restaurants list according to number of reviews
    def sort_eventsList_city(self):
        self.eventsList.sort(key= lambda x:str(x.city_name), reverse=True)
  
    # Define method to sort restaurants list according to rating
    def sort_eventsList_numcomments(self):
        self.eventsList.sort(key= lambda x:int(str(x.comment_count)), reverse=True)
        
    # Define method to sort restaurants list according to rating
    def sort_eventsList_startime(self):
        self.eventsList.sort(key= lambda x:str(x.start_time), reverse=True)




