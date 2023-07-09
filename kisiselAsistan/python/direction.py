# Python Flask code

from flask import Flask, request, jsonify, send_from_directory
import os
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask(__name__, static_folder='build_direction/static')


@app.route('/directions', methods=['POST'])
def get_directions():
    data = request.get_json()
    start_location = data['startLocation']
    end_location = data['endLocation']

    geolocator = Nominatim(user_agent="directions_app")

    # Get the coordinates of the start location
    start_location = geolocator.geocode(start_location, country_codes="TR")
    start_latitude = start_location.latitude
    start_longitude = start_location.longitude

    # Get the coordinates of the end location
    end_location = geolocator.geocode(end_location, country_codes="TR")
    end_latitude = end_location.latitude
    end_longitude = end_location.longitude

    # Calculate the distance between the two locations
    distance = geodesic((start_latitude, start_longitude), (end_latitude, end_longitude)).kilometers

    # Calculate the duration between the two locations (assuming default speed of 80 km/h)
    speed = 80  # km/h
    duration = distance / speed

    # Create a response object
    response = {
        'distance': f'{distance:.2f} km',
        'duration': f'{duration:.2f} hours',
        'coordinates': [(start_latitude, start_longitude), (end_latitude, end_longitude)]
    }

    return jsonify(response)


# React dosyalarını sunmak için route
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("build_direction/" + path):
        return send_from_directory("build_direction/", path)
    else:
        return send_from_directory("build_direction", "index.html")


if __name__ == '__main__':
    app.run()
