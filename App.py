import json
from Tracker import Tracker
from Thread import Thread


class App:

	def __init__(self):

		self.__trackers = []

		with open('trackers.json') as file:

			obj = json.load(file)

			for tracker in obj['trackers'].values():

				self.__trackers.append(Tracker(tracker['_Tracker__name'], tracker['_Tracker__URL'], tracker['_Tracker__email'], tracker['_Tracker__desirePrice'], tracker['_Tracker__price']))

		self.__options = {

			-1: {

				"description": "Exit"

			},
			0: {

				"description": "See trackers",
				"method": self.displayTrackers

			},
			1: {

				"description": "Add tracker",
				"method": self.addTracker

			},
			2: {

				"description": "Remove tracker",
				"method": self.removeTracker

			},
			3: {

				"description": "Start thread",
				"method": self.startThread

			},
			4: {

				"description": "Stop thread",
				"method": self.stopThread

			}

		}

		self.__thread = None

	def run(self):

		while True:

			self.displayOptions()
			option = int(input('Enter option number: '))

			if option == -1:

				if self.__thread is not None:

					self.__thread.stop()
					self.__thread.join()

					self.__thread = None

				print('Bye')
				break

			else:

				if option in self.__options.keys():

					self.__options[option]['method']()

				else:

					print('Invalid option')

	def displayOptions(self):

		for option in self.__options:

			print(f'{option} - {self.__options[option]["description"]}')

	def displayTrackers(self):

		print('index - code - name - desirePrice - price - URL')

		for index, tracker in enumerate(self.__trackers):

			print(f'{index} - {tracker.getCode()} - {tracker.getName()} - {tracker.getDesirePrice()} - {tracker.getPrice()} - {tracker.getURL()}')

	def addTracker(self):

		name = input('Enter tracker name: ')
		URL = input('Enter tracker URL: ')
		email = input('Enter email to notify: ')
		desirePrice = float(input('Enter desire price: '))

		newTracker = Tracker(name, URL, email, desirePrice)

		newTracker.addTracker()
		self.__trackers.append(newTracker)

		if self.__thread:

			self.__thread.updateTrackers(self.__trackers)

	def removeTracker(self):

		self.displayTrackers()
		trackerIndex = int(input('Enter tracker index to remove: '))

		if trackerIndex > -1 and trackerIndex < len(self.__trackers):

			removeTracker = self.__trackers[trackerIndex]

			removeTracker.removeTracker()
			del self.__trackers[trackerIndex]

			if self.__thread:

				self.__thread.updateTrackers(self.__trackers)

		else:

			print('Invalid index')

	def startThread(self):

		if self.__thread is None:

			thread = Thread(self.__trackers)
			self.__thread = thread

			self.__thread.start()

			print('Thread enabled')

		else:

			print('Thread already enabled')

	def stopThread(self):

		if self.__thread is not None:

			self.__thread.stop()
			self.__thread.join()

			self.__thread = None

			print('Thread stopped')

		else:

			print('No thread')