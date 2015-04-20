"""
Ridership vs. Temp Correlation
"""

import pickle

#load weather data
from weather_collection import WeatherDatum
weather = pickle.load(open('weatherDataFile', 'rb'))

#load hubway data
hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))

print "everything is loaded"

def count_riders(year, month, day, hour):
	"""
	Input: year, month, day, hour
	Output: total riders during that hour
	"""
	counter = 0
	for minute in range(0,60):
		print (year, month, day, hour, minute)
		if hubway.data[year][month][day+1][hour][minute] == -1:
			pass
		else:
			counter += len(hubway.data[year][month][day+1][hour][minute])
	return counter

def start(year):
	"""
	Combines ridership and temperature data into a list of tuples.
	"""

	if year % 4 == 0:
		numDaysInMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	else:
		numDaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

	riders_vs_temp = {}

	#first, add all temps to dict as keys with values 0
	#then, add riders to associated keys

	for m in range(1,13):
		for d in range(numDaysInMonth[m-1]):
			for h in range(0,24):
				riders_vs_temp[weather.data[year][m][d+1][h]['tempi']] = 0

	for month in range(1,13):
		for day in range(numDaysInMonth[month-1]):
			for hour in range(24):
				riders_vs_temp[weather.data[year][month][day+1][hour]['tempi']] += count_riders(year, month, day, hour)

	return riders_vs_temp

print start(2013)

def test():
	pass