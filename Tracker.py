import json
import hashlib
import time

class Tracker:

	def __init__ (self, name, URL, price):
		self.code = hashlib.md5(URL.encode()).hexdigest()
		self.name = name
		self.URL = URL
		self.price = price
		self.createdTimestamp = time.time()
		self.lastUpdateTimestamp = time.time()

	def addTracker(self):

		with open('trackers.json') as file:

			obj = json.load(file)

			if (not self.code in obj['trackers']):

				obj['trackers'][self.code] = (self.__dict__)

				with open('trackers.json', 'w') as file:

					json.dump(obj, file, indent = '\t')

					print('Tracker added correctly')

			else:

				print('Tracker already exists')

	def updateTracker(self):

		with open('trackers.json') as file:

			obj = json.load(file)

			obj['lastUpdateTimestamp'] = time.time()

			if (self.code in obj['trackers']):

				self.lastUpdateTimestamp = time.time()

				obj['trackers'][self.code] = (self.__dict__)

				with open('trackers.json', 'w') as file:

					json.dump(obj, file, indent = '\t')

					print('Tracker updated correctly')

			else:

				print('Tracker do not exists')

	def removeTracker(self):

		with open('trackers.json') as file:

			obj = json.load(file)

			if (not self.code in obj['trackers']):

				del obj['trackers'][self.code]

				with open('trackers.json', 'w') as file:

					json.dump(obj, file, indent = '\t')

					print('Tracker removed correctly')

			else:

				print('Tracker do not exists')

	def setName(self, name):
		self.name = name
		self.updateTracker()

	def setURL(self, URL):
		self.URL = URL
		self.updateTracker()

	def setPrice(self, price):
		self.price = price
		self.updateTracker()

	def seeTracker(self):
		print(self.code, " - " + self.URL, " - ", self.price)