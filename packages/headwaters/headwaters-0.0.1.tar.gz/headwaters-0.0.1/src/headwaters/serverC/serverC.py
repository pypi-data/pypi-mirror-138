from flask import Flask, jsonify
from flask_socketio import SocketIO
import json

with open('src/headwaters/serverC/data.json') as f:
    data = f.read()

app = Flask('serverC')
sio = SocketIO(app)

@app.get('/')
def index():
    return jsonify(serverC="says hello")

def run():
    print(data)
    sio.run(app, debug=False)