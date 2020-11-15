from flask import Flask, render_template, request, redirect, url_for
import requests, json
import datetime
from datetime import datetime, date, timedelta
import calendar

app = Flask(__name__)


@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template('form.html')

@app.route("/temperature", methods= ["POST", "GET"])
def temperature():
    msg = ""
    zipcode = request.form['zip']
    res = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+'&units=imperial&appid=d6c3883364ca9dae46be60aa932ad58b')
    json_object = res.json()
    try :
        temp_f = float(json_object['main']['temp'])
        mintemp = float(json_object['main']['temp_min'])
        maxtemp = float(json_object['main']['temp_max'])
            
        mintemp = round(mintemp, 2)
        maxtemp = round(maxtemp, 2)
        temp_f = round(temp_f, 2)

        description = json_object['weather'][0]['description']
        humidity = json_object['main']['humidity']
        cityName = json_object['name']
        ws = json_object['wind']['speed']
        sunrise = json_object['sys']['sunrise']
        sunset = json_object['sys']['sunset']
        sunrise = datetime.fromtimestamp(sunrise).strftime('%I:%M%p')
        sunset = datetime.fromtimestamp(sunset).strftime('%I:%M%p')

        obj = {
            "temp": temp_f,
            "zipcode": zipcode,
            "maxtemp": maxtemp, 
            "mintemp":mintemp, 
            "descr":description, 
            "hum": humidity,
            "cityName": cityName,
            "ws" : ws,
            "rise" : sunrise,
            "set" : sunset,
        }

    except(KeyError):
        obj = {""}
        msg = "No weather info for " + str(zipcode)

  
    return render_template("temp.html", obj = obj, message = msg)


@app.route("/5day3hour", methods= ["POST", "GET"])
def weeklyTemperature():
    msg = ""
    zipcode = request.form['zip']
    res = requests.get('http://api.openweathermap.org/data/2.5/forecast?zip='+zipcode+'&units=imperial&appid=d6c3883364ca9dae46be60aa932ad58b')
    json_object = res.json()

    try:
        day1 = {}
        day2 = {}
        day3 = {}
        day4 = {}
        day5 = {}

        for i in json_object['list']:
            today = datetime.now().date()
            dtstring = i['dt_txt']
            dtStamp = datetime.strptime(dtstring, "%Y-%m-%d %H:%M:%S")
            dateF = dtStamp.date()
            dateAsString = dateF.strftime("%a, %b %d")
            dateT = dtStamp.strftime("%I:%M%p") 
            weekNumber = dateF.weekday()
            weekName = calendar.day_name[weekNumber]
            description = i['weather'][0]['description']
            iconUrl = "http://openweathermap.org/img/wn/"+i['weather'][0]['icon']+".png"
            if today + timedelta(days=1) == dateF:
                day1[dateT] = i['main']['temp']
                day1["date"] = dateAsString
                day1["dayOfWeek"] = weekName
                day1[dateT + "d" ] = description
                day1[dateT + "icon"] = iconUrl
            elif today + timedelta(days=2) == dateF:
                day2[dateT] = i['main']['temp']
                day2["date"] = dateAsString
                day2["dayOfWeek"] = weekName
                day2[dateT + "d" ] = description
                day2[dateT + "icon"] = iconUrl
            elif today+ timedelta(days=3) == dateF:
                day3[dateT] = i['main']['temp']
                day3["date"] = dateAsString
                day3["dayOfWeek"] = weekName
                day3[dateT + "d" ] = description
                day3[dateT + "icon"] = iconUrl
            elif today+ timedelta(days=4) == dateF:
                day4[dateT] = i['main']['temp']
                day4["date"] = dateAsString
                day4["dayOfWeek"] = weekName
                day4[dateT + "d" ] = description
                day4[dateT + "icon"] = iconUrl
            elif today+ timedelta(days=5) == dateF:
                day5[dateT] = i['main']['temp']
                day5["date"] = dateAsString
                day5["dayOfWeek"] = weekName
                day5[dateT + "d" ] = description
                day5[dateT + "icon"] = iconUrl
        obj = {
            "city" : json_object['city']['name'],
            "country" : json_object['city']['country'],
            "day1" : day1,
            "day2" : day2,
            "day3" : day3,
            "day4" : day4,
            "day5" : day5
        }

    except(KeyError):
        obj = {""}
        msg = "No extended weather info for " + str(zipcode)

  
    return render_template("weektemp.html", obj = obj, message = msg)





if __name__=='__main__' :
    app.run(debug=True)