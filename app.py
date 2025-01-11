from flask import Flask, render_template,request
import requests
import os
from time import time
from dotenv import load_dotenv

app=Flask(__name__)

load_dotenv()

api_key=os.getenv('API_KEY_OpenWeather')

@app.route('/home',methods=["POST","GET"])
def home():
    if request.method=="POST":
        city_name=request.form.get('city_name')
        weather_api_url=f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={api_key}"
        response=requests.get(weather_api_url).json()
        if response['cod']=="200":
            temperature=response['list'][0]['main']['temp']
            min_temperature=response['list'][0]['main']['temp_min']
            max_temperature=response['list'][0]['main']['temp_max']
            description=response['list'][0]['weather'][0]['description']
            icon=response['list'][0]['weather'][0]['icon']
            last_refreshed=response['list'][0]['dt_txt']
            return render_template('index.html',city_name=city_name.capitalize(),temperature=temperature,min_temperature=min_temperature,max_temperature=max_temperature,description=description,icon=icon,last_refreshed=last_refreshed,current_time=time())
        else:
            return "Not able to access the API"
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)