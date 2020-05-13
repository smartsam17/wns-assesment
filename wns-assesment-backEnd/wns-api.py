from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import pymongo
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time 
import gevent
app = Flask(__name__)
from threading import Thread
app.config['SECRET_KEY'] = 'sachin!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_timeout=30, logger=False, engineio_logger=False)

myclient = pymongo.MongoClient("mongodb://sachin17:Sapple123!@ds125953.mlab.com:25953/homoeopathy_in_kanpur")
mydb = myclient["homoeopathy_in_kanpur"]

thread = None
serverName = 'server1'

@app.route('/')
def index():
    return "Hello"

 
@socketio.on('connect')
def con():
    seversThread()
        
def seversThread():
    global thread
    if thread is None:
        thread = Thread(target=background_task)
        thread.start()

def background_task():
    with app.app_context():
        while True:
           time.sleep(5)
           get_servers()


def get_servers():
    print('Client connected')
    servers = []
    mycol = mydb["servers"]
    #global serverName
    #serverName = 'server1'
    print(serverName)
    query = {"serverName": serverName}
    for x in mycol.find(query):
        record = {"serverName": x["serverName"], "cpu": x["cpu"], "ram": x["ram"], "network": x["network"]}
        servers.append(record)
    print(record)    
    emit('response', {'data': servers}, broadcast=True, namespace='/')



@socketio.on('getServerName', namespace='/')
def get_server(message):
    #emit('my response', {'data': message['data']})
    #print(message['data'])
    global serverName
    serverName = message['data']
    background_task(ss)

@socketio.on('disconnect', namespace='/')
def disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')




    