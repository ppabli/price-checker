import json
import hashlib
import time
import re
import requests
from config import config
import smtplib
from bs4 import BeautifulSoup as beautifulSoup
import ssl

class Tracker:

	"""Tracker class
	Version: 0.1
	Author: Pablo Liste Cancela
	Last update: 22/06/2020
	"""

	def __init__ (self, name, URL, email, desirePrice, price = -1):

		self.__code = hashlib.md5(URL.encode()).hexdigest()
		self.__createdTimestamp = time.time()
		self.__lastUpdateTimestamp = time.time()

		self.__name = name
		self.__URL = URL
		self.__email = email
		self.__desirePrice = desirePrice

		self.__price = price

	def addTracker(self):

		with open('trackers.json') as file:

			obj = json.load(file)

			if (not self.__code in obj['trackers']):

				obj['lastUpdateTimestamp'] = time.time()
				obj['trackers'][self.__code] = self.__dict__

				with open('trackers.json', 'w', encoding = 'utf8') as file:

					json.dump(obj, file, indent = '\t')

					print('Tracker added correctly')

			else:

				print('Tracker already exists')

	def updateTracker(self):

		with open('trackers.json') as file:

			obj = json.load(file)

			if (self.__code in obj['trackers']):

				self.__lastUpdateTimestamp = time.time()

				obj['lastUpdateTimestamp'] = time.time()
				obj['trackers'][self.__code] = (self.__dict__)

				with open('trackers.json', 'w', encoding = 'utf8') as file:

					json.dump(obj, file, indent = '\t')

					print('Tracker updated correctly')

			else:

				print('Tracker do not exists')

	def removeTracker(self):

		with open('trackers.json') as file:

			obj = json.load(file)

			if self.__code in obj['trackers']:

				del obj['trackers'][self.__code]
				obj['lastUpdateTimestamp'] = time.time()

				with open('trackers.json', 'w', encoding = 'utf8') as file:

					json.dump(obj, file, indent = '\t')

					print('Tracker removed correctly')

			else:

				print('Tracker do not exists')

	def trackPrice(self):

		with open('webs.json') as file:

			obj = json.load(file)

			for web in obj.keys():

				if (re.search(web, self.__URL)):

					page = requests.get(self.__URL, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
					soup1 = beautifulSoup(page.content, 'html.parser')
					soup2 = beautifulSoup(soup1.prettify(), "html.parser")
					element = soup2.find(id = obj[web]['element'])

					if (element):

						text = element.getText()
						text2 = text.strip().replace(",", ".")
						price = float(re.sub('$|€', '', text2))

						self.__price = price

						if (self.__price <= self.__desirePrice):

							self.sendEmail();

						self.updateTracker()

					else:

						print('No element detected')

					break

			else:

				print('No web detetected')

		print('Track done')

	def sendEmail(self):

		try:

			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.ehlo()

			server.login(config['email'], config['emailPassword'])

			subject = f'The product {self.__name} has dropped in price.'
			body = f'This is an automated message from price tracker.\nThe product{self.__name} with code: {self.__code} it has dropped in price and now it costs {self.__price} euros.\nCheck the product in this link {self.__URL}'

			message = f"Subject: {subject}\n\n{body}".encode('utf-8')
			server.sendmail(

				config['email'],
				self.__email,
				message

			)

			print('Email sended')

		except:

			print('Error on email')

		finally:

			return server.quit()

	def getCode(self):

		return self.__code

	def getName(self):

		return self.__name

	def getURL(self):

		return self.__URL

	def getEmail(self):

		return self.__email

	def getDesirePrice(self):

		return self.__desirePrice

	def getPrice(self):

		return self.__price

	def setName(self, name):

		self.__name = name
		self.updateTracker()

	def setEmail(self, email):

		self.__email = email
		self.updateTracker()

	def setDesirePrice(self, desirePrice):

		self.__desirePrice = desirePrice
		self.updateTracker()
