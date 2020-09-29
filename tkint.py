#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:12:44 2020

@author: ratan
"""

import datetime
import time
import tkinter as tk
from tkinter import *
from tkinter import font 
from PIL import Image, ImageTk

import trip_planner as tp

# Defining the height and width of GUI 
HEIGHT = 1000
WIDTH = 1000

# Defining some global parameters which would be used to parse the parameters received through GUI buttoms
YELP_DATE=""
YELP_TIME=""
YELP_UNIX_TIME = 0
YELP_REST_CATG = "" 
LOC_YELP = ""
KWRDS_EVENTS = "" 
TEXT_FOR_LABEL = ""

# Below are API keys needed for this project
YELPK = "" 
HIKEK = ""
EVENTK = "" 

class TKGUI: 
    
    def __init__(self,root= ""):
        self.root = root

    def get_unix_time():
        global YELP_TIME
        global YELP_DATE
        global YELP_UNIX_TIME 
        if YELP_DATE !=" ":
            if YELP_TIME != "":
                dspl = YELP_DATE.split("/")
                year = int(dspl[0])
                month = int(dspl[1])
                day = int(dspl[2])
                tspl = YELP_TIME.split(":")
                hour = int(tspl[0])
                mins = int(tspl[1])
                dt = datetime.datetime(year,month,day,hour,mins)
                #print("Unix Timestamp: ",(time.mktime(dt.timetuple())))
                YELP_UNIX_TIME = int(time.mktime(dt.timetuple()))
     
    # Method to set the time to go to restaurant           
    def set_time_yelp(entry):
        global YELP_TIME
        YELP_TIME = entry
        TKGUI.get_unix_time()
        
    # Method to get the Yelp date
    def set_date_yelp(entry):
        global YELP_DATE
        YELP_DATE = entry
        
    # Method to set the restaurant category
    def set_YELP_REST_CATG(entry): 
        global YELP_REST_CATG
        YELP_REST_CATG = entry 
        
    def set_LOC_YELP(entry):
        global LOC_YELP
        LOC_YELP = entry 
        
    def set_events_kwrds(entry):
        global KWRDS_EVENTS
        KWRDS_EVENTS = entry 
        
    def clear():
        global t1
        global lower_frame
        t1.delete(1.0,END)
        
    # Method for presenting the Yelp data 
    def present_yelp_data(sr,t1): 
        global YELP_UNIX_TIME
        global YELP_REST_CATG
        global LOC_YELP 
        global TEXT_FOR_LABEL
        global YELPK
        #print("Yelp key is",YELPK)
        ye = tp.yelp(YELPK)
        print("Trip unix time received:", YELP_UNIX_TIME)
        print("Yelp Restaurant category:", YELP_REST_CATG)
        print("Yelp location provided:", LOC_YELP)
        print("\nPrinting the names of top 10 restaurants found in the search location and category:")
        ye.set_business_params(search_term=YELP_REST_CATG,loc=LOC_YELP,op_at=YELP_UNIX_TIME)
        ye.set_all_business_det()
        TEXT_FOR_LABEL = ""
        
        if sr == 1: 
            ye.sort_restsList_numreviews()
        elif sr == 2:
            ye.sort_restsList_rating()
        elif sr == 3: 
            ye.sort_restsList_distance()
        
        for rest in ye.restsList:
            TEXT_FOR_LABEL = TEXT_FOR_LABEL + str(rest.name)+", City:"+str(rest.city)+", Zip:"+str(rest.zip)+", Distance:"+str(rest.distance)+", Rating:"+str(rest.rating)+", #Reviews:"\
                +str(rest.review_count)+"\n\n"
                
        t1.delete(1.0,END)
        t1.insert(INSERT, TEXT_FOR_LABEL)
        print("\nDone setting the parameters and presenting the Yelp data\n\n")
    
    
    # Method for presenting the Hiking Data
    def present_hike_data(sr,t1):
        global LOC_YELP
        global TEXT_FOR_LABEL
        global HIKEK
        print("\nPrinting the names of top 10 hiking locations found in search category")
        hp = tp.hikeproject(hid=HIKEK,loc=LOC_YELP)
        hp.set_lat_long()
        hp.set_hike_params()
        TEXT_FOR_LABEL = "" 
        if sr == 1: 
            hp.sort_hikesiteList_starvotes()
        elif sr == 2:
            hp.sort_restsList_stars()
        elif sr == 3: 
            hp.sort_restsList_length()
        
        for hke in hp.hikesiteList:
            TEXT_FOR_LABEL = TEXT_FOR_LABEL+str(hke.name)+", Location:"+str(hke.location)+", Difficulty:"+str(hke.difficulty)+", Length:"+str(hke.length)\
                +", Stars:"+str(hke.stars)+", StarVotes:"+str(hke.starVotes)+"\n\n" 
        t1.delete(1.0,END)
        t1.insert(INSERT, TEXT_FOR_LABEL)
        print("\nDone setting the parameters and presenting the hike locations data")
        
    # Method for presenting the Events data
    def present_events_data(sr,t1):
        global LOC_YELP
        global KWRDS_EVENTS
        global TEXT_FOR_LABEL
        global EVENTK
        global YELP_DATE
        print("\nPrinting the names of top 10 events in listed category and date")
        #eventKey = tp.get_eventful_api.get_api_key()
        ev = tp.eventful(EVENTK)
        ev.set_event_params(kwds=KWRDS_EVENTS,loc=LOC_YELP,edate=YELP_DATE)
        TEXT_FOR_LABEL = ""
        if sr == 1: 
            ev.sort_eventsList_city()
        elif sr == 2:
            ev.sort_eventsList_numcomments()
        elif sr == 3: 
            ev.sort_eventsList_startime()
        
        for event in ev.eventsList:
            TEXT_FOR_LABEL = TEXT_FOR_LABEL+str(event.title)+", Venue:"+str(event.venue_name)+"\n----->Address:"+str(event.venue_address)+", City:"+str(event.city_name)+\
                "\n----->NumComments:"+str(event.comment_count)+" Start:"+str(event.start_time)+', Stop:'+str(event.stop_time)+"\n\n"
        t1.delete(1.0,END)
        t1.insert(INSERT, TEXT_FOR_LABEL)
    
        TEXT_FOR_LABEL = ""
        print("\nDone setting the parameters and presenting the events data\n")
    

    def build(self):

        lower_frame = tk.Frame(self.root, bg='#94b8b8', bd=5)
        lower_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.4, anchor='n')
    
        # Text to be displayed in TK 
        t1 = tk.Text(lower_frame, font=('Times New Roman',20), fg='#0073e6')
        t1.place(relwidth=1, relheight=1)
    
    
        frame1 = tk.Frame(self.root, bg='#94b8b8', bd=5)
        frame1.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.05, anchor='n')
        
        entry1 = tk.Entry(frame1, font=40)
        entry1.place(relx=0.5, relwidth=0.5, relheight=1)
        
        
        button1 = tk.Button(frame1, text="Trip Location ((Region State Country) OR Zip)", font=40, command= lambda: TKGUI.set_LOC_YELP(entry1.get()))
        button1.place(relx=0, relheight=1, relwidth=0.5)
        
        frame11 = tk.Frame(self.root, bg='#94b8b8', bd=5)
        frame11.place(relx=0.5, rely=0.15, relwidth=0.75, relheight=0.05, anchor='n')
        
        entry11 = tk.Entry(frame11, font=40)
        entry11.place(relx=0.5, relwidth=0.5, relheight=1)
        
        
        button11 = tk.Button(frame11, text="Date of Trip (YYYY/MM/DD)", font=40, command= lambda: TKGUI.set_date_yelp(entry11.get()))
        button11.place(relx=0, relheight=1, relwidth=0.5)
        
        frame12 = tk.Frame(self.root, bg='#94b8b8', bd=5)
        frame12.place(relx=0.5, rely=0.2, relwidth=0.75, relheight=0.05, anchor='n')
        
        entry12 = tk.Entry(frame12, font=40)
        entry12.place(relx=0.5, relwidth=0.5, relheight=1)
        
        
        button12 = tk.Button(frame12, text="Time for Dinner (HH:MM)", font=40, command= lambda: TKGUI.set_time_yelp(entry12.get()))
        button12.place(relx=0, relheight=1, relwidth=0.5)
        
        frame2 = tk.Frame(self.root, bg='#94b8b8', bd=5)
        frame2.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.05, anchor='n')
        
        entry2 = tk.Entry(frame2, font=40)
        entry2.place(relx=0.5, relwidth=0.5, relheight=1)
        
        
        button2 = tk.Button(frame2, text="Yelp Restaurant Category", font=40, command= lambda: TKGUI.set_YELP_REST_CATG(entry2.get()))
        button2.place(relx=0, relheight=1, relwidth=0.5)
        
        frame24 = tk.Frame(self.root, bg='#94b8b8', bd=5)
        frame24.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.05, anchor='n')
        
        entry24 = tk.Entry(frame24, font=40)
        entry24.place(relx=0.5, relwidth=0.5, relheight=1)
        
        
        button24 = tk.Button(frame24, text="Events Keywords", font=40, command= lambda: TKGUI.set_events_kwrds(entry24.get()))
        button24.place(relx=0, relheight=1, relwidth=0.5)
        
        
        
        frame22 = tk.Frame(self.root, bg='#94b8b8', bd=5)
        frame22.place(relx=0.5, rely=0.35, relwidth=0.75, relheight=0.05, anchor='n')
        
        
        button22 = tk.Button(frame22, text="Yelp Data", font=("bold",16), fg='#0073e6', command= lambda: TKGUI.present_yelp_data(0,t1))
        button22.place(relx=0.1, relheight=1, relwidth=0.2)
        
        button221 = tk.Button(frame22, text="Sortby_ReviewCount", font=40, command= lambda: TKGUI.present_yelp_data(1,t1))
        button221.place(relx=0.3, relheight=1, relwidth=0.2)
        
        button222 = tk.Button(frame22, text="Sortby_Rating", font=40, command= lambda: TKGUI.present_yelp_data(2,t1))
        button222.place(relx=0.5, relheight=1, relwidth=0.2)
        
        button223 = tk.Button(frame22, text="Sortby_Distance", font=40, command= lambda: TKGUI.present_yelp_data(3,t1))
        button223.place(relx=0.7, relheight=1, relwidth=0.2)
        
        frame3 = tk.Frame(self.root, bg='#94b8b8', bd=5)
        frame3.place(relx=0.5, rely=0.4, relwidth=0.75, relheight=0.05, anchor='n')
        
        
        button3 = tk.Button(frame3, text="Hiking Data", font=("bold",16), fg='#0073e6', command= lambda: TKGUI.present_hike_data(0,t1))
        button3.place(relx=0.1, relheight=1, relwidth=0.2)
        
        button31 = tk.Button(frame3, text="Sortby_StarVotes", command= lambda: TKGUI.present_hike_data(1,t1))
        button31.place(relx=0.3, relheight=1, relwidth=0.2)
        
        button32 = tk.Button(frame3, text="Sortby_Stars", command= lambda: TKGUI.present_hike_data(2,t1))
        button32.place(relx=0.5, relheight=1, relwidth=0.2)
        
        button33 = tk.Button(frame3, text="Sortby_length", command= lambda: TKGUI.present_hike_data(3,t1))
        button33.place(relx=0.7, relheight=1, relwidth=0.2)
        
        frame4 = tk.Frame(self.root, bg='#94b8b8', bd=5)
        frame4.place(relx=0.5, rely=0.45, relwidth=0.75, relheight=0.05, anchor='n')
        
        
        button4 = tk.Button(frame4, text="Events Data", font=("bold",16), fg='#0073e6', command= lambda: TKGUI.present_events_data(0,t1))
        button4.place(relx=0.1, relheight=1, relwidth=0.2)
        
        button41 = tk.Button(frame4, text="Sortby_City", command= lambda: TKGUI.present_events_data(1,t1))
        button41.place(relx=0.3, relheight=1, relwidth=0.2)
        
        button42 = tk.Button(frame4, text="Sortby_NumComment", command= lambda: TKGUI.present_events_data(2,t1))
        button42.place(relx=0.5, relheight=1, relwidth=0.2)
        
        button43 = tk.Button(frame4, text="Sortby_StartTime", command= lambda: TKGUI.present_events_data(3,t1))
        button43.place(relx=0.7, relheight=1, relwidth=0.2)
        
        upper_frame = tk.Frame(self.root, bg='#94b8b8', bd=5)
        upper_frame.place(relx=0.5, rely=0.02, relwidth=0.75, relheight=0.05, anchor='n')
        
        labelnew = tk.Label(upper_frame, font=("Times New Roman bold",26), bg='#e6e6e6')
        labelnew.place(relwidth=1, relheight=1)
        
        labelnew['text'] = "Welcome to Trip Planner GUI"


def main(): 
    global YELPK
    global HIKEK
    global EVENTK
    print("For this project, you need API keys for yelp.com, hikingporject.com and Eventful.com")
    YELPK = input("Enter API key for yelp.com ")
    HIKEK = input("Enter API key for hikingproject.com ")
    EVENTK = input("Enter API key for eventful.com ")
    print("Loading the GUI for Trip Planner")
    root = tk.Tk()
    root.title("Trip Planner")
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    background_image = tk.PhotoImage(file='gui_pic.png')
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    canvas.pack()
    tkg = TKGUI(root)
    tkg.build()
    root.mainloop()

if __name__ == '__main__':
    main()

    
