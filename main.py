from flask import Flask
from flask_restful import Resource, Api
import time
import requests
import threading


files = {"Val150":None, "Val151":None, "Val250":None, "Val251":None, "Val252":None, "Val253":None, "Val350":None, "Val351":None, "Val352":None, "Val353":None, "T290":None, "T291":None, "T292":None, "T293":None, "T390":None, "T391":None, "T392":None, "T393":None}
fileText = {"Val150":"", "Val151":"", "Val250":"", "Val251":"", "Val252":"", "Val253":"", "Val350":"", "Val351":"", "Val352":"", "Val353":"", "T290":"", "T291":"", "T292":"", "T293":"", "T390":"", "T391":"", "T392":"", "T393":""}

app = Flask(__name__)
api = Api(app)


refreshRate = 1 #seconds


# @app.before_first_request
def activate():
	def updateData():
		while True:
			for key, value in files.items():
				value.seek(0);
				fileText[key] = value.read()
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
		files[key] = open(key,"r")

	activate()

	app.run(debug=True)



