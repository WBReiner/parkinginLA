import numpy as np
import os
import requests
import predict
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
from string import Template
import psycopg2
import urllib.parse as urlparse
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
from IPython.core.display import display, HTML


app = Flask(__name__)
url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )
            
def cluster_id(lat,long,wday):
    #user_input_coords 
    u_lat=str(lat)
    u_lon=str(long)
    u_day=str(wday)
    app_user_query = "SELECT parkingresults.*, ST_Distance(geog, poi)/1000 AS distance_km FROM parkingresults, (select ST_MakePoint( '"+u_lon+"','"+u_lat+"')::geography as poi) as poi WHERE ST_DWithin(geog, poi, 1000) ORDER BY ST_Distance(geog, poi) LIMIT 3;"
    user_SUBSET = pd.read_sql_query(app_user_query,con)
    #user_SUBSET=user_SUBSET[user_SUBSET['violationdescription'].str.contains("NO PARK/STREET CLEAN")==False]
    if u_day == "All days":
        day_select=user_SUBSET
    else:
        day_select=user_SUBSET[user_SUBSET['day'].str.contains(u_day)==True]
    day_specifics=day_select[['hour','violationdescription', 'result', 'weekdayindex']]
    day_specifics.columns=['Hour', 'Description', 'Result', 'Day']
    df=day_specifics
    df['bins'] = np.digitize(np.asarray(df['Result'], dtype = 'float'), np.asarray([1, 1.1, 5.1,10,26,51,76]))
    df['daybins'] = np.digitize(np.asarray(df['Day'], dtype = int), np.asarray([1,2,3,4,5,6,7,]))
    dict_parking = {0: 'You can relax! You have a lower risk than average in all of Los Angeles.', 1: 'Equal risk compared to Los Angeles average.', 2: 'Very low risk; risk of this violation is less than 10% higher than Los Angeles average.', 3: 'Slight caution is recommended, there is a 10-25% higher risk of being issued this type of parking violation.', 4:"High risk! You'd better get back to your car on time & carefully inspect posted parking signs. You are in a high-risk area where this type of violation is issued at a rate > 50% the Los Angeles average.", 5: "HIGHEST RISK. You need to proceed with caution and make sure you are following all parking rules. There is a >75% risk of getting this type of parking ticket relative to the Los Angeles average."}
    dict_hour = {0: '12:00 AM - 6:00 AM', 1: '12:00 AM - 6:00 AM', 2: '12:00 AM - 6:00 AM', 3: '12:00 AM - 6:00 AM',  4: '12:00 AM - 6:00 AM', 5: '12:00 AM - 6:00 AM', 6: '6:00 AM - 7:00 AM', 7: '7:00 AM - 8:00 AM', 8: '8:00 AM - 9:00 AM', 9: '9:00 AM - 10:00 AM', 10: '10:00 AM - 11:00 AM', 11: '11:00 AM - 12:00 PM', 12: '12:00 PM - 2:00 PM', 13: '12:00 PM - 2:00 PM', 14: '2:00 PM - 4:00 PM', 15: '2:00 PM - 4:00 PM', 16: '4:00 PM - 6:00 PM', 17: '4:00 PM - 6:00 PM', 18: '6:00 PM - 8:00 PM', 19: '6:00 PM - 8:00 PM', 20: '8:00 PM - 10:00 PM', 21: '8:00 PM - 10:00 PM', 22: '10:00 PM - 12:00 AM', 23: '10:00 PM - 12:00 AM'}
    dict_days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
    df['Day'] = df['daybins'].map(dict_days)
    df['Display']=df['bins'].map(dict_parking)
    df['Hour_better'] = df['Hour'].map(dict_hour)
    displays = [] # initialize a list for displaying
    for cat in list(set(df['Display'])):
        df_tmp = df[df['Display'] == cat]
        displays.append(list(zip(list(df_tmp['Hour_better']), list(df_tmp['Display']), list(df_tmp['Description']), list(df_tmp['Day']))))
    finalanswer=displays[0:15]
    return finalanswer

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
    	lat = request.form['lat']
    	long = request.form['lng']
    	wday = request.form['weekday']
    	print(lat, long, wday)
    	lat = float(lat)
    	long = float(long)
    	#returns finalanswer
    	calc = cluster_id(str(lat), str(long), wday)
        
        # return redirect(url_for('index'))
    	return render_template('results.html', lat=lat, long=long, calc=calc, wday=wday)
    key=os.environ['API_KEY']
    return render_template('savedhtml.html',key=key)
    
@app.route('/geocode', methods = ['POST'])
def geocode():
    address = request.get_json()['address']
    bounds = request.get_json()['bounds']
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&bounds={}&key={}'.format(address, bounds, os.environ['API_KEY']))
    return jsonify(r.text)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    