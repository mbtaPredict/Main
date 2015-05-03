import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
import ast
import time
from pprint import pprint
import pickle


WUNDERGROUND_API_KEY = "3ec21efc1c37b8b2"
WUNDERGROUND_BASE_URL = "http://api.wunderground.com/api/"+WUNDERGROUND_API_KEY


def get_json(url):
	"""
	Input: url
	Output: .json string from the url
	"""

	#Open the API value of the url and return as .json
	f = urllib2.urlopen(str(url))
	return json.loads(f.read())


def weather_on(date):
	"""
	Input: past date (yyyymmdd)
	Output: hourly weather data on that day
	"""

	#Return .json of weather in Boston, MA on the specified date
	return get_json(WUNDERGROUND_BASE_URL+ "/history_" + str(date) + "/q/MA/Boston.json")


def store_year_data(year):
	"""
	Stores the hourly weather data for <YEAR> and stores it as 365 separate
		.txt files in a folder called '<YEAR>Data'. The folder called
		'<YEAR>Data' needs to be made before hand by the user.
	"""

	#Variable that keeps the code from running accidentally (set to False to run code)
	SAFETY = True

	#The starting date variables
	month = 1
	day = 1

	#Lists defining the number of days in each of the 12 months
	month31 = [1, 3, 5, 7, 8, 10, 12]
	month30 = [4, 6, 9, 11]
	month28 = [2]
	if year % 4 == 0:
		numDaysFeb = 29
	else:
		numDaysFeb = 28

	#List used to convert numbers to 2 digit strings
	number = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
			  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
			  '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

	#Access the Wunderground data and archives it to a text file for every day in a year
	if SAFETY == False:
		for x in range(12):
			day = 1
			if month in month31:
				for x in range(31):
					date = str(year)+number[month]+number[day]
					f = open('WeatherData/'+str(year)+'Data/'+str(year)+'-'+number[month]+'-'+number[day]+'.txt', 'w')
					f.write(str(weather_on(date)))
					f.close()
					time.sleep(6)
					day += 1
			elif month in month30:
				for x in range(30):
					date = str(year)+number[month]+number[day]
					f = open('WeatherData/'+str(year)+'Data/'+str(year)+'-'+number[month]+'-'+number[day]+'.txt', 'w')
					f.write(str(weather_on(date)))
					f.close()
					time.sleep(6)
					day += 1
			elif month in month28:
				for x in range(numDaysFeb):
					date = str(year)+number[month]+number[day]
					f = open('WeatherData/'+str(year)+'Data/'+str(year)+'-'+number[month]+'-'+number[day]+'.txt', 'w')
					f.write(str(weather_on(date)))
					f.close()
					time.sleep(6)
					day += 1
			month += 1


def archived_day(year, month=-1, day=-1):
	"""
	Input: string of past date that you want to acces the weather data of
		('yyyy-mm-dd' OR 'yyyy', 'mm', 'dd')
	Output: hourly weather data from archives
	"""

	#Convert inputs to strings and integers
	year = str(year)
	month = int(month)
	day = int(day)

	#Converts month and day into 2 digit integers
	month = "%02d" % month
	day = "%02d" % day

	#If statements that sort out the format of the input
	if '-' in year:
		f = open('WeatherData/'+year[:4]+'Data/'+year+'.txt')
		weatherData = f.read()
		weatherData = ast.literal_eval(weatherData)
		return weatherData
	else:
		f = open('WeatherData/'+year+'Data/'+year+'-'+month+'-'+day+'.txt')
		weatherData = f.read()
		weatherData = ast.literal_eval(weatherData)
		return weatherData


def archived_hour(year, month, day, hour):
	"""
	Input: past hour that you want to access the weather data of
		('yyyy', 'mm', 'dd', 'hh' *in military time betweeen 00 and 23)
	Output: dictionary of weather data of that hour from the archives
	"""

	#Convert inputs to strings and integers
	year = str(year)
	month = int(month)
	day = int(day)
	hour = int(hour)

	#Converts month and day into 2 digit integers
	month = "%02d" % month
	day = "%02d" % day
	hour = "%02d" % hour

	#Create a list of weather data for all hours of the specified day (each hour is a
	#	dictionary that occupies one index in the list)
	dayData = archived_day(year, month, day)
	hoursListData = dayData['history']['observations']
	startFound = False

	#Find the first time that is an hour before the specified time
	for x in xrange(len(hoursListData)):
		if int(hour) == 0:
			start = 0
			startFound = True
			break
		elif int(hoursListData[x]['date']['hour']) == int(hour)-1:
			start = x
			startFound = True
			break

	#If the code does not find a place to start, then run this backup code
	if not startFound:
		for x in xrange(len(hoursListData)):
			if int(hoursListData[x]['date']['hour']) == int(hour)-2:
				start = x
				startFound = True
				break

	#If the code STILL does not find a place to start, have it start from hour 00
	if not startFound:
		start = 0
		print "ERROR 404: START NOT FOUND ON", year, month, day, hour

	#Find the index of the time closest to the desired time
	correctHourIndex = 0
	if int(hour) != 0:
		error = 60
		correctHourIndex = len(hoursListData)-1
		for x in xrange(len(hoursListData)-start-1):
			if int(hoursListData[start+x]['date']['hour']) < int(hour):
				NewError = 60-int(hoursListData[start+x]['date']['min'])
			else:
				NewError = int(hoursListData[start+x]['date']['min'])
			if NewError > error:
				correctHourIndex = start + x -1
				break
			else:
				error = NewError

	return hoursListData[correctHourIndex]


class WeatherDatum:
	def __init__(self):
		self.data = {}

	def add_year(self, year):
		"""
		Input: integer for year you want to add weather data for(we have to
			have the weather data already stored for that year)
		Output: stores the weather data for that year in the class
		"""

		if year % 4 == 0:
			numDaysInMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		else:
			numDaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		self.data[year] = {}
		for month in xrange(12):
			self.data[year][month+1] = {}
			for day in xrange(numDaysInMonth[month]):
				self.data[year][month+1][day+1] = {}
				for hour in xrange(24):
					self.data[year][month+1][day+1][hour] = archived_hour(year, month+1, day+1, hour)


def get_imminent_weather(year, month, day, hour):
	"""
	Input: ints for year, month, day, hour (this time must be within
		the next 10 days)
	Output: the dictionary of weather data for that hour
	"""

	data = get_json(WUNDERGROUND_BASE_URL+'/hourly10day/q/MA/Boston.json')
	for hourData in data['hourly_forecast']:
		if int(hourData['FCTTIME']['mon']) == month:
			if int(hourData['FCTTIME']['mday']) == day:
				if int(hourData['FCTTIME']['hour']) == 12:
					return hourData


def get_imminent_temp(year, month, day, hour):
	"""
	Input: ints for year, month, day, hour (this time must be within
		the next 10 days)
	Output: integer for forecasted temp at the given hour in degrees fahrenheit
	"""

	data = get_imminent_weather(year, month, day, hour)
	return int(data['temp']['english'])


def get_imminent_temp_precip_snow(year, month, day, hour):
	"""
	Input: ints for year, month, day, hour (this time must be within
		the next 10 days)
	Output: list of forcasted temperature in degrees, precipitation in inches, and snow (0 or 1)
	"""

	data = get_imminent_weather(year, month, day, hour)
	return [float(data['temp']['english']), float(data['qpf']['english']), int(data['snow']['english'] == 0)]

# RUN THIS TO OPEN THE WEATHER DATABASE CLASS STRUCTURE:
# ----------------------------------------------------
# weather = pickle.load(open('LargeDataStorage/weatherDataFile', 'rb'))
# ----------------------------------------------------

# RUN THIS TO RE-SAVE THE WEATHER DATA TO THE PICKLE FILE:
# ----------------------------------------------------
# pickle.dump(weather, open('LargeDataStorage/weatherDataFile', 'wb'))
# ----------------------------------------------------