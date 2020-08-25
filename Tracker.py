import hashlib
import time
import re
import requests
import smtplib
from bs4 import BeautifulSoup as beautifulSoup
import ssl

import config


class Tracker:

	"""Tracker class
	Version: 0.2
	Author: Pablo Liste Cancela
	Last update: 22/06/2020
	"""

	def __init__ (self, name, url, webData, email, desirePrice, price = -1):

		self.__code = hashlib.md5(url.encode()).hexdigest()
		self.__createdTimestamp = time.time()
		self.__lastUpdateTimestamp = time.time()

		self.__name = name
		self.__url = url
		self.__webData = webData
		self.__email = email
		self.__desirePrice = desirePrice

		self.__price = price

	def trackPrice(self):

		page = requests.get(self.__url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
		soup1 = beautifulSoup(page.content, "html.parser")
		soup2 = beautifulSoup(soup1.prettify(), "html.parser")

		element = soup2.find(self.__webData["tag"], attrs = self.__webData["attributes"])

		if (element):

			if self.__webData["inside"] == False:

				text = element.getText()

			else:

				text = element[self.__webData["inside"]]

			text2 = text.strip().replace(",", ".")
			price = float(re.sub("$|€", '', text2))

			self.__price = price

			if (self.__price <= self.__desirePrice):

				self.sendEmail();

			else:

				print("No element detected")

		else:

			print("No web detetected")

		print("Track done")

	def sendEmail(self):

		try:

			server = smtplib.SMTP("smtp.gmail.com", 587)
			server.ehlo()
			server.starttls()
			server.ehlo()

			server.login(config.EMAILADDRESS, config.EMAILPASSWORD)

			subject = f"The product {self.__name} has dropped in price."
			body = f"This is an automated message from price tracker.\nThe product{self.__name} with code: {self.__code} it has dropped in price and now it costs {self.__price} euros.\nCheck the product in this link {self.__url}"

			message = f"Subject: {subject}\n\n{body}".encode("utf-8")
			server.sendmail(

				config.EMAILADDRESS,
				self.__email,
				message

			)

			print("Email sended")

		except:

			print("Error on email")

		finally:

			return server.quit()

	def getCode(self):

		return self.__code

	def getName(self):

		return self.__name

	def getURL(self):

		return self.__url

	def getEmail(self):

		return self.__email

	def getDesirePrice(self):

		return self.__desirePrice

	def getPrice(self):

		return self.__price

	def setName(self, name):

		self.__name = name

	def setEmail(self, email):

		self.__email = email

	def setDesirePrice(self, desirePrice):

		self.__desirePrice = desirePrice