
import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import requests


app = Flask (__name__)
model = joblib.load('power_prediction.sav')


@app.route('/')
def home():
    return render_template('intro.html')
@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/windapi', methods=['POST'])
def windapi():
    city = request.form.get('city')

    f=open(r"D:/Docu/pyjunb/API_keys/weather api.txt")
    apikey=f.read()

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}"

    resp = requests.get(url)
    resp_json = resp.json()

    temp_kelvin = resp_json["main"]["temp"]
    temp_celsius = round(temp_kelvin - 273.15, 2)  # Convert to Celsius
    humid = str(resp_json["main"]["humidity"]) + " %"
    pressure = str(resp_json["main"]["pressure"]) + " mmHG"
    wind_speed = float(resp_json["wind"]["speed"])
    wind_speed_str = str(wind_speed)  # numeric value for input

    # Simple example theoretical power curve based on wind speed
    def get_theoretical_power(ws):
        if ws < 3:
            return 0
        elif ws < 5:
            return 50
        elif ws < 8:
            return 150
        elif ws < 12:
            return 300
        else:
            return 500

    theoretical_power = get_theoretical_power(wind_speed)

    return render_template(
        'predict.html',
        temp=f"{temp_celsius} °C",
        humid=humid,
        pressure=pressure,
        speed=str(wind_speed) + " m/s",
        wind_speed_value=wind_speed,          # auto-fill wind speed
        theoretical_power=theoretical_power   # auto-fill theoretical power
    )


@app.route('/y_predict', methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[float(x) for x in request.form.values()]]
    prediction = model.predict(x_test)
    print(prediction)
    output=prediction [0]
    return render_template('predict.html', prediction_text='The energy predicted is {:.2f} KWh'.format(output))

if __name__ == "__main__":
    app.run(debug=False)