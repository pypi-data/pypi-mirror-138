import os
import pandas as pd
import numpy as np
import sys
from datetime import date as dt
from datetime import timedelta as td 
import time
from time import sleep
import datetime
from dateutil import parser
import pytz
import requests
import math



"""

MANDATORY INNPUT: token, api_key

OPTIONAL INPUT:

- start: n days ago for starting the date range.
        Default start = 7 days ago.
        
- end: n days ago for ending the date range.
        Default end = 0 days ago.


"""



def get_aircall_calls(token, api_key, #mandatory
                      
                      start = 7, end = 0 #optional
                     ):

    contacts_lenght = 0
    records = []

    start_date = (dt.today()-td(days = start)).isoformat()
    
    
    print("start {} days ago: {}".format(start, start_date))
    
    # converted to UNIX timefromat 
    start_date =math.trunc(time.mktime(datetime.datetime.strptime(start_date, "%Y-%m-%d").timetuple()))

    
    
    
    end_date = (dt.today()-td(days = end)).isoformat()
    
    print("end {} days ago: {}".format(end, end_date))
    
    # converted to UNIX timefromat 
    
    end_date = math.trunc(time.mktime(datetime.datetime.strptime(end_date, "%Y-%m-%d").timetuple()))


    page = 1

    contacts_lenght = 0
    records = []


    while True :

        if page%15 == 0: 
            print("Page N.", page)

        sleep(1)
        link = f'https://{token}:{api_key}@api.aircall.io/v1/calls?from={start_date}&to={end_date}&page={page}&per_page=20'
        headers = {'accept': 'application/json'}
        response = requests.request("GET", link, headers=headers)
        dati = response.json()
        dati_meta = 0
        if dati['meta']['count'] == 0 :
            dati_meta = 1
        else :
            dati_meta = dati['meta']['count'] 
    # increments contacts_lenght 
        contacts_lenght +=   dati_meta
        page = page + 1
        if contacts_lenght <= dati['meta']['total'] :
            for d in dati['calls']:

                try:
                    id = d['id']
                except:
                    id  = ''
                try:
                    cost_cent = d['cost']
                except:
                    cost_cent  = ''                
                try:
                    direction = d['direction']
                except:
                    direction  = ''
                try:
                    status = d['status']
                except:
                    status  = ''
                try:
                    started_at = d['started_at']
                except:
                    started_at  = ''
                try:
                    answered_at = d['answered_at']
                except:
                    answered_at  = ''
                try:
                    ended_at = d['ended_at']
                except:
                    ended_at  = ''
                try:
                    duration = d['duration']
                except:
                    duration  = ''
                try:
                    raw_digits = d['raw_digits']
                except:
                    raw_digits  = ''
                try:
                    user_id = d['user'][0]['id']
                except:
                    try:
                        user_id  = d['user']['id']
                    except:

                        user_id = ''
                try:
                    user_name = d['user'][0]['name']
                except:
                    try:
                        user_name  = d['user']['name']
                    except:
                        user_name = ''
                try:
                    contact_id = d['contact']['id']
                except:
                    contact_id  = ''
                try:
                    contact_name = d['contact']['first_name']
                except:
                    contact_name  = ''
                try:
                    contact_last_name = d['contact']['last_name']
                except:
                    contact_last_name  = ''
                try:
                    cnt_company_name = d['contact']['company_name']
                except:
                    cnt_company_name  = ''

                records.append({
                    'id' : id,
                    'direction' : direction,
                    'status' : status,
                    'started_at' : started_at, #
                    'answered_at' : answered_at, #
                    'ended_at' : ended_at,
                    'duration' : duration, #
                    'raw_digits' : raw_digits, #deal_id
                    'user_id' : user_id,
                    'user_name' : user_name,
                    'contact_id' : contact_id,
                    'contact_name' : contact_name,
                    'contact_last_name' : contact_last_name,
                    'cnt_company_name' : cnt_company_name,
                    'cost_cent' : cost_cent
                })      
        else :
            break


    aircall_calls = pd.DataFrame(records)


    unix_to_readable = ["answered_at", "ended_at", "started_at"]

    for unix_col in unix_to_readable:

        aircall_calls[unix_col] = pd.to_datetime(aircall_calls[unix_col], unit='s')


    return aircall_calls