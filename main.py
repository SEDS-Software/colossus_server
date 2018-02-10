from flask import Flask
from flask_restful import Resource, Api
import time
import requests
import threading
from flask_cors import CORS


files = {"Val150":None, "Val151":None, "Val250":None, "Val251":None, "Val252":None, "Val253":None, "Val350":None, "Val351":None, "Val352":None, "Val353":None, "T290":None, "T291":None, "T292":None, "T293":None, "T390":None, "T391":None, "T392":None, "T393":None, "Tank_Temp_1":None, "Tank_Temp_2":None, "Battery":None, "Thrust":None, "SeqStage":None}

# Not yet mapped, uncomment when mapped
# for i in range(2):
# 	files["E0" + str(i + 1)] = None
# for i in range(8):
# 	files["W0" + str(i + 1)] = None
# files["Tank_Fuel_1"]=None
# files["Tank_Fuel_2"]=None


for i in range(14):
	files["PT" + str(i + 1)] = None

del(files["PT8"])


fileText = {}


app = Flask(__name__)
CORS(app)
api = Api(app)


refreshRate = 1 #seconds


# @app.before_first_request
def activate():
	def updateData():
		while True:
			for key, value in files.items():
				value.seek(0)
				val = value.read()
				fileText[key] = val[:len(val) - 1]
			time.sleep(refreshRate)
	thread = threading.Thread(target=updateData)
	thread.start()



class HelloWorld(Resource):
	def get(self):
		return fileText


api.add_resource(HelloWorld, '/')


# def start_runner():
# 	def start_loop():
# 		not_started = True
# 		while not_started:
# 			print('in start loop')
# 			try:
# 				r = requests.get('http://127.0.0.1:5000/')
# 				if r.status_code == 200:
# 					print("server started")
# 					not_started = False
# 			except Exception as e:
# 				print("server not yet started")
# 			time.sleep(2)
# 	thread = threading.Thread(target=start_loop)
# 	thread.start()

if __name__ == '__main__':
	for key, value in files.items():
		try:
			files[key] = open(key,"r")
		except:
			print("missing file")

	activate()

	app.run(host='0.0.0.0')



