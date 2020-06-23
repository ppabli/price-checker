import threading
import time


class Thread(threading.Thread):

	def __init__(self, trackers, *args, **kwargs):

		super(Thread, self).__init__(*args, **kwargs)
		self.__stopFlag = False
		self.__trackers = trackers

	def run(self):

		while not self.__stopFlag:

			for tracker in self.__trackers:

				tracker.trackPrice()

			i = 0
			while not self.__stopFlag and i <= 12 * 60 * 60:

				i += 1
				time.sleep(1)

	def stop(self):

		self.__stopFlag = True

	def updateTrackers(self, trackers):

		self.__trackers = trackers
