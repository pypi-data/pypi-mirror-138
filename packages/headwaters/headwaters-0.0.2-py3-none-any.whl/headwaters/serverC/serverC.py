from flask import Flask, jsonify
from flask_socketio import SocketIO
import json

import os

path = os.path.relpath(__file__)
dir = os.path.dirname(path)

print(f"rel path is {path} and dir is {dir}")

with open(f"{dir}/data.json") as f:
    data = f.read()

app = Flask('serverC')
sio = SocketIO(app)

@app.get('/')
def index():
    return jsonify(serverC="says hello")

def run():
    print(data)
    sio.run(app, debug=False)