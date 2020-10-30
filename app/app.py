from flask import Flask, render_template, request, redirect, url_for
import requests, json
import datetime

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
        sunrise = datetime.datetime.fromtimestamp(sunrise).strftime('%H:%M')
        sunset = datetime.datetime.fromtimestamp(sunset).strftime('%H:%M')

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


if __name__=='__main__' :
    app.run(debug=True)