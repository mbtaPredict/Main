import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
import ast
import time
from pprint import pprint

WUNDERGROUND_API_KEY = "3ec21efc1c37b8b2"
WUNDERGROUND_BASE_URL = "http://api.wunderground.com/api/"+WUNDERGROUND_API_KEY

MBTA_API_KEY = "KE_VanziA0OQ_r_sV6_KIQ"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/"

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
	Stores the hourly weather data for <YEAR> and stores it as 365 separate .txt files in a folder
	called '<YEAR>Data'.
	"""

	#Variable that keeps the code from running accidentally (set to False to run code)
	SAFETY = False

	#The starting date variables
	month = 1
	day = 1

	#Lists defining the number of days in each of the 12 months
	month31 = [1, 3, 5, 7, 8, 10, 12]
	month30 = [4, 6, 9, 11]
	month28 = [2]
	month29 = []

	#List used to convert numbers to 2 digit strings
	number = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
			  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
			  '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

	#Access the Wunderground data and archives it for every day in a year
	if SAFETY == False:
		for x in range(12):
			day = 1
			if month in month31:
				for x in range(31):
					date = str(year)+number[month]+number[day]
					f = open(str(year)+'Data/'+str(year)+'-'+number[month]+'-'+number[day]+'.txt', 'w')
					f.write(str(weather_on(date)))
					f.close()
					# time.sleep(6)
					day += 1
			elif month in month30:
				for x in range(30):
					date = str(year)+number[month]+number[day]
					f = open(str(year)+'Data/'+str(year)+'-'+number[month]+'-'+number[day]+'.txt', 'w')
					f.write(str(weather_on(date)))
					f.close()
					# time.sleep(6)
					day += 1
			elif month in month28:
				for x in range(29):
					date = str(year)+number[month]+number[day]
					f = open(str(year)+'Data/'+str(year)+'-'+number[month]+'-'+number[day]+'.txt', 'w')
					f.write(str(weather_on(date)))
					f.close()
					# time.sleep(6)
					day += 1
			month += 1


def archived_day(year, month=-1, day=-1):
	"""
	Input: past date that you want to acces the weather data of ('yyyy-mm-dd' OR 'yyyy', 'mm', 'dd')
	Output: hourly weather data from archives
	"""

	#If statements sort out the format of the input
	if '-' in year:
		f = open(year[:4]+'Data/'+year+'.txt')
		weatherData = f.read()
		weatherData = ast.literal_eval(weatherData)
		return weatherData
	else:
		f = open(year+'Data/'+year+'-'+month+'-'+day+'.txt')
		weatherData = f.read()
		weatherData = ast.literal_eval(weatherData)
		return weatherData


def archived_hour(year, month, day, hour):
	"""
	Input: past hour that you want to access the weather data of ('yyyy', 'mm', 'dd', 'hh'
		   *in military time betweeen 00 and 23)
	Output: dictionary of weather data of that hour from the archives
	"""

	#Create a list of weather data for all hours of the specified day (each hour is a
	#	dictionary that occupies one index in the list)
	dayData = archived_day(year, month, day)
	hoursListData = dayData['history']['observations']

	#Find the first time that is an hour before the specified time
	for x in xrange(len(hoursListData)):
		if int(hour) == 0:
			start = 0
			break
		elif int(hoursListData[x]['date']['hour']) == int(hour)-1:
			start = x
			break

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


def hour_summary(year, month, day, hour):
	"""
	Input: past hour that you want to access the weather data of ('yyyy', 'mm', 'dd', 'hh'
		   *in military time betweeen 00 and 23)
	Output: summary of weather data of that hour from the archives
	"""

	#Makes the dictionary of data into a string split into lines
	hourData = str(archived_hour(year, month, day, hour))
	hourData = hourData.replace(", '", '\n')
	hourData = hourData.replace("{", '\n')
	hourData = hourData.replace("'", '')
	hourData = hourData.replace("}", '')
	return hourData


def stuff():
	f = open('HubwayData/2011_hubway_trips.csv', 'r')
	hubwayData = f.read()
	hubwayData = hubwayData.split('\n')
	for x in xrange(len(hubwayData)):
		hubwayData[x] = hubwayData[x].split(',')
	# for x in hubwayData:
	# 	if len(hubwayData[x]>0):
	# 		rideData.append(hubwayData[x])
	return len(hubwayData)

store_year_data(2012)