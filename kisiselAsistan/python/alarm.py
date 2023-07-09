from flask import Flask, request, jsonify, send_from_directory
import datetime
import time
import threading
import pygame
import os

app = Flask(__name__, static_folder='build_alarm/static')

alarms = []

def play_alarm(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

def set_alarm(alarm_time, sound_file):
    current_time = datetime.datetime.now().time()
    alarm_time_obj = datetime.datetime.strptime(alarm_time, '%H:%M').time()

    while current_time < alarm_time_obj:
        time.sleep(1)
        current_time = datetime.datetime.now().time()

    t = threading.Thread(target=play_alarm, args=(sound_file,))
    t.start()

@app.route('/alarms', methods=['GET', 'POST', 'DELETE'])
def handle_alarms():
    global alarms

    if request.method == 'GET':
        return jsonify(alarms)
    elif request.method == 'POST':
        data = request.get_json()
        alarm_time = data.get('time')
        sound_file = os.path.join('sounds', data.get('sound'))

        alarms.append({'time': alarm_time, 'sound': sound_file})
        t = threading.Thread(target=set_alarm, args=(alarm_time, sound_file))
        t.start()

        return jsonify(alarms)
    elif request.method == 'DELETE':
        alarm_time = request.args.get('time')

        alarms = [alarm for alarm in alarms if alarm['time'] != alarm_time]

        return jsonify(alarms)


# React dosyalarını sunmak için route
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("build_alarm/" + path):
        return send_from_directory("build_alarm/", path)
    else:
        return send_from_directory("build_alarm", "index.html")


if __name__ == '__main__':
    pygame.init()
    alarms = []
    app.run(debug=True)

