from ast import excepthandler
from crypt import methods
from logging import exception
from urllib import response
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response, Response
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



def ConvertTimeTo12Hour(time):
    format = '%Y-%m-%d %H:%M' #specifify the format of the date_string.
    date = datetime.strptime(time, format)
    dateForUpdateTime = datetime.strptime(time, format)

    convertedTime = dateForUpdateTime.strftime('%I:%M %p')


    return convertedTime


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
    #cond = load['current']['condition']['text']
    windSpeedNoRound = load['current']['wind_mph']
    humidity = load['current']['humidity']
    cloudCover = load['current']['cloud']
    country = load['location']['country']
    cityTime = load['location']['localtime']
    updateTime = load['current']['last_updated']
    uv = load['current']['uv']
    cond = 'Cloudy'
        

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

    return (tempRound, cond, windSpeed, humidity, cloudCover, country, cityTime, lastUpdateTime, uv, city, cityDate)






@app.route('/')
def hello_world():
    return redirect(url_for('home'))

#____________________MAIN ROUTE_______________
@app.route('/home', methods = ['GET', 'POST'])
def home():

    
    #Free IP fetch API
    url = 'https://ipapi.co/json/'
    
    r = requests.get(url)
    j = json.loads(r.text)
    city = j['city']
    


    apiTester = apiDump(city=city)
    



   
    
    if request.method == 'POST':
        cityRaw = request.form.get('search')
        city = cityRaw.title()

        apiTester = apiDump(city=city)


    resp = make_response(render_template('index.html', data = apiTester))

    resp.set_cookie('city', city)

    return resp


def ConvertDateTimeToDay(dateTime):
    format = '%Y-%m-%d %H:%M' 

    date = datetime.strptime(dateTime, format)

    cityDate = date.strftime('%A, %d %b %Y')

    return cityDate




def apiDump(city):

    

    key = '4116a68b717644c3917221856222607'
    apiCallCurrent = 'current.json'

    weatherURL = requests.get('https://api.weatherapi.com/v1/'+apiCallCurrent+'?key='+key+'&q='+city)
    weatherdata = weatherURL.json

    url2 = 'https://api.weatherapi.com/v1/'+apiCallCurrent+'?key='+key+'&q='+city
    req = requests.get(url2)
    
    load = json.loads(req.text)

    
    
    

    data = {

        "temp": round(load['current']['temp_c']),
        "cond": load['current']['condition']['text'],
        "humidity": load['current']['humidity'],
        "cloudCover": load['current']['cloud'],
        "windSpeed": round(load['current']['wind_mph']),
        "cityTime": ConvertTimeTo12Hour(load['location']['localtime']),
        "updateTime": ConvertTimeTo12Hour(load['current']['last_updated']),
        "uv": int(load['current']['uv']),
        "country": load['location']['country'],
        "cityDate": ConvertDateTimeToDay(load['location']['localtime']),
        "city" : city
        
    }
    

    return data
    


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    
