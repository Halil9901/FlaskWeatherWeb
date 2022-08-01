from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import timeago



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

@app.route('/api')
def apiCall():
    city = 'Oxford'

    key = '4116a68b717644c3917221856222607'
    apiCallCurrent = 'current.json'

   
    
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


    
    else:   
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

    timeAgo = (timeago.format(updatetimeFormat, now)) 
    
    

    return jsonify(tempRound, cond, windSpeed, humidity, cloudCover, country, cityTime, updateTime, uv)


    
    




@app.route('/')
def hello_world():
    return redirect(url_for('home'))


@app.route('/home', methods = ['GET', 'POST'])
def home():

    
    #IP fetch API
    #url = 'https://ipapi.co/json/'
    
    #r = requests.get(url)
    #j = json.loads(r.text)
    # city = j['city']
    city = 'Oxford'

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
    conditionstr = str(cond[0]) 
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
        conditionstr = str(cond[0]) 
        cityTime = load['location']['localtime']
        updateTime = load['current']['last_updated']
        uv = load['current']['uv']


    format = '%Y-%m-%d %H:%M' #specifify the format of the date_string.

    updatetimeFormat = datetime.strptime(updateTime, format)
    now = datetime.now()

    

    date = datetime.strptime(cityTime, format)
    cityTime = date.strftime('%I:%M %p')
    cityDate = date.strftime('%A, %d %b %Y')

    uv = int(uv)

    timeAgo = (timeago.format(updatetimeFormat, now)) 
    

        

    tempRound = round(temp)
        
    windSpeed = round(windSpeedNoRound)
    # Change back to conditionstr
    FakeCond = 'Sunny'
    


    return render_template('index.html',country=country,humidity=humidity ,cloudCover=cloudCover, 
      windSpeed=windSpeed,
      city=city, temp=tempRound, cond=FakeCond,
      day=day, date=date, localtime=localtime, uv=uv, 
      cityTime=cityTime, cityDate=cityDate, timeAgo=timeAgo)


@app.route('/test', methods=['GET'])
def index():
    city = 'Oxford'
    key = '4116a68b717644c3917221856222607'
    apiCallCurrent = 'current.json'

    url2 = 'https://api.weatherapi.com/v1/'+apiCallCurrent+'?key='+key+'&q='+city

    req = requests.get(url2)
    load = json.loads(req.text)
    temp = load['current']['temp_c']
    cond = load['current']['condition']['text']

    return jsonify(cond)

@app.route('/date', methods=['GET'])
def date():

    city = 'Oxford'
    key = '4116a68b717644c3917221856222607'
    apiCallCurrent = 'current.json'

    url2 = 'https://api.weatherapi.com/v1/'+apiCallCurrent+'?key='+key+'&q='+city

    req = requests.get(url2)
    load = json.loads(req.text)
    temp = load['current']['temp_c']
    cond = load['current']['condition']['text']
    cityTime = load['location']['localtime']
    updateTime = load['current']['last_updated']


    

    format = '%Y-%m-%d %H:%M' #specifify the format of the date_string.

    date = datetime.strptime(updateTime, format)
    currentTime = date.strftime('%I:%M %p')
    updateMinute = date.strftime('%M')
    updateMinuteInt = int(updateMinute)
    cityDate = date.strftime('%A, %d %b %Y')
    now = datetime.now()
    yesterday = now - timedelta(minutes=30)
    timeAgo = (timeago.format(date, now)) 

    return jsonify(timeAgo)

