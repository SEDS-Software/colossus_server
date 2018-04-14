from flask import Flask
from flask_restful import Resource, Api
import time
import requests
import threading
from flask_cors import CORS
import PyQStationConnect.PyQStationConnect as Qstation
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from ctypes import*
import ctypes



GINSDll = ctypes.cdll.LoadLibrary("giutility.dll")

labels = []
values = []
buffers = []
global value_map
value_map = {}

def setup():
    try:
        conn = [Qstation.ConnectGIns(0),Qstation.ConnectGIns(1),Qstation.ConnectGIns(2)]
        for c in conn:
            c.init_connection("192.168.1.28")
            c.read_sample_rate()
            self=c
            if(c.read_channel_count() != ""):
                for i in range(int(c.read_channel_count())):
                    GINSDll._CD_eGateHighSpeedPort_GetDeviceInfo(self.HCONNECTION.value,self.Channel_InfoName,i,None,self.char)
                    label=self.char.value.decode('UTF-8')
                    if (label!='Timestamp'):
                        labels.append(self.char.value.decode('UTF-8'))
                buffers.append(c.yield_buffer())
                print(buffers)

    except Exception as e:
        print(e)
        time.sleep(20)
        print("RETRY")
        setup()

setup()

def update_values():
    values = []
    try:
        for buffer in buffers:
                data = []
                while(len(data) == 0):
                        data = next(buffer)
                        
                ## Get mean over all the rows
                data = np.array(data)
                data = np.mean(data, axis=0)
                data = np.delete(data, 0)
                for d in data:
                        values.append(d)
        global value_map
        value_map = dict(zip(labels, values))
    except StopIteration:
        print("why are you running htis")
        buffers.clear()
        time.sleep(1)
        print("REDID IT")
        setup()



app = Flask(__name__)
CORS(app)
api = Api(app)


refreshRate = .2 #seconds


def activate():
    def updateData():
        while True:
            update_values()
            time.sleep(refreshRate)
    thread = threading.Thread(target=updateData)
    thread.start()



class HostsCrap(Resource):
    def get(self):
        global value_map
        return value_map


api.add_resource(HostsCrap, '/')
update_values()


if __name__ == '__main__':

    activate()

    app.run(host='0.0.0.0')
