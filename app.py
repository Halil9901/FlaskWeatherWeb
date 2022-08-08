from crypt import methods
from urllib import response
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from flask_cors import CORS
import timeago
import os



from datetime import datetime, timedelta
import time
import calendar
import requests
import json
app = Flask(__name__)



app.secret_key = 'Brookes3099'
today = datetime.today()
curr_date = datetime.today()
now = datetime.now()

day = calendar.day_name[curr_date.weekday()]
date = today.strftime("%d, %B %Y")
localtime = time.asctime( time.localtime(time.time()) )







@app.route('/update_api', methods = ['GET', 'POST'])
def apiUpdate():
    api = apiData()
   


    return jsonify(api)



def apiData():
    city = request.cookies.get('city')

    key = '4116a68b717644c3917221856222607'
    apiCallCurrent = 'current.json'

    url2 = 'https://api.weatherapi.com/v1/'+apiCallCurrent+'?key='+key+'&q='+city
    req = requests.get(url2)
    load = json.loads(req.text)
    req = requests.get(url2)
    load = json.loads(req.text)
    temp = load['current']['temp_c']
    cond = load['current']['condition']['text']
    windSpeedNoRound = load['current']['wind_mph']
    humidity = load['current']['humidity']
    cloudCover = load['current']['cloud']
    country = load['location']['country']
    cityTime = load['location']['localtime']
    updateTime = load['current']['last_updated']
    uv = load['current']['uv']
        

    windSpeed = round(windSpeedNoRound)
    tempRound = round(temp)

    format = '%Y-%m-%d %H:%M' #specifify the format of the date_string.

    updatetimeFormat = datetime.strptime(updateTime, format)
    now = datetime.now()

        

    date = datetime.strptime(cityTime, format)
    cityTime = date.strftime('%I:%M %p')
    cityDate = date.strftime('%A, %d %b %Y')

    uv = int(uv)

    dateForUpdateTime = datetime.strptime(updateTime, format)
    lastUpdateTime = dateForUpdateTime.strftime('%I:%M %p')

    timeAgo = (timeago.format(updatetimeFormat, now)) 

    

   

    return (tempRound, cond, windSpeed, humidity, cloudCover, country, cityTime, lastUpdateTime, uv, city, cityDate)






    
    


@app.route('/')
def hello_world():
    return redirect(url_for('home'))

#____________________MAIN ROUTE_______________
@app.route('/home', methods = ['GET', 'POST'])
def home():

    
    #IP fetch API
    #url = 'https://ipapi.co/json/'
    
    #r = requests.get(url)
    #j = json.loads(r.text)
    # city = j['city']
    city = 'London'

    #WeatherAPI fetch weather data in C

    key = '4116a68b717644c3917221856222607'
    apiCallCurrent = 'current.json'


    url2 = 'https://api.weatherapi.com/v1/'+apiCallCurrent+'?key='+key+'&q='+city
    req = requests.get(url2)
    load = json.loads(req.text)
    req = requests.get(url2)
    load = json.loads(req.text)
    temp = load['current']['temp_c']
    cond = load['current']['condition']['text']
    windSpeedNoRound = load['current']['wind_mph']
    humidity = load['current']['humidity']
    cloudCover = load['current']['cloud']
    country = load['location']['country']
    cityTime = load['location']['localtime']
    updateTime = load['current']['last_updated']
    uv = load['current']['uv']

   
    
    if request.method == 'POST':
        cityRaw = request.form.get('search')
        city = cityRaw.title()
        url2 = 'https://api.weatherapi.com/v1/'+apiCallCurrent+'?key='+key+'&q='+city

        req = requests.get(url2)
        load = json.loads(req.text)
        temp = load['current']['temp_c']
        cond = load['current']['condition']['text']
        windSpeedNoRound = load['current']['wind_mph']
        humidity = load['current']['humidity']
        cloudCover = load['current']['cloud']
        country = load['location']['country']
        cityTime = load['location']['localtime']
        updateTime = load['current']['last_updated']
        uv = load['current']['uv']
        city1 = session['city'] 


    windSpeed = round(windSpeedNoRound)
    tempRound = round(temp)

    format = '%Y-%m-%d %H:%M' #specifify the format of the date_string.

    updatetimeFormat = datetime.strptime(updateTime, format)
    now = datetime.now()

        

    date = datetime.strptime(cityTime, format)
    cityTime = date.strftime('%I:%M %p')
    cityDate = date.strftime('%A, %d %b %Y')

    dateForUpdateTime = datetime.strptime(updateTime, format)
    lastUpdateTime = dateForUpdateTime.strftime('%I:%M %p')

    uv = int(uv)

    timeAgo = (timeago.format(updatetimeFormat, now)) 
    

    resp = make_response(render_template('index.html',country=country,humidity=humidity ,cloudCover=cloudCover, 
      windSpeed=windSpeed,
      city=city, temp=tempRound, cond=cond,
      day=day, date=date, localtime=localtime, uv=uv, 
      cityTime=cityTime, cityDate=cityDate, lastUpdateTime=lastUpdateTime))

    resp.set_cookie('city', city)
    
    
    
    
    
    


    return resp

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
