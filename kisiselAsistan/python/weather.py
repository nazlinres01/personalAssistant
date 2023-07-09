from flask import Flask, jsonify, send_from_directory, request
import os
import requests
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='build_weather/static')


@app.route('/api/weather')
def get_weather():
    api_key = 'eb4084523d66ce8652c09dbdfa962406'  # OpenWeatherMap API anahtarını buraya girin
    city = request.args.get('city', '')  # Kullanıcının istediği şehri al

    if not city:
        return jsonify({'error': 'City parameter is missing'})

    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

    response = requests.get(current_weather_url)
    if response.status_code == 200:
        data = response.json()
        if data.get('cod') == '404':
            return jsonify({'error': 'City not found'})

        temperature = data.get('main', {}).get('temp')
        condition = data.get('weather', [{}])[0].get('description')
        icon = data.get('weather', [{}])[0].get('icon')

        result = {
            'city': city,
            'temperature': temperature,
            'condition': condition,
            'icon': icon
        }

        forecast_response = requests.get(forecast_url)
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            forecast_list = forecast_data.get('list', [])

            forecast = []
            today = datetime.now().date()

            for i in range(7):
                date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
                forecast_day = [item for item in forecast_list if item.get('dt_txt', '').startswith(date)]

                if not forecast_day:
                    continue

                temperature = forecast_day[0].get('main', {}).get('temp')
                condition = forecast_day[0].get('weather', [{}])[0].get('description')
                icon = forecast_day[0].get('weather', [{}])[0].get('icon')

                forecast.append({
                    'date': date,
                    'temperature': temperature,
                    'condition': condition,
                    'icon': icon
                })

            result['forecast'] = forecast

        return jsonify(result)
    else:
        return jsonify({'error': 'Failed to fetch weather'})


# React dosyalarını sunmak için route
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("build_weather/" + path):
        return send_from_directory("build_weather/", path)
    else:
        return send_from_directory("build_weather", "index.html")


if __name__ == '__main__':
    app.run()