"""
Ridership vs. Temp Correlation
"""

import pickle
import matplotlib.pyplot as plt
from numpy import linspace
from pylab import *

#load weather data
from weather_collection import WeatherDatum
weather = pickle.load(open('weatherDataFile', 'rb'))

#load hubway data
hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))


def count_riders(year, month, day, hour):
	"""
	Input: year, month, day, hour
	Output: total riders during that hour
	"""

	#initialize counter
	counter = 0

	#counts riders during a given hour
	for minute in range(0,60):
		#-1 means that there is no data for that time, so we don't count that
		if hubway.data[year][month][day+1][hour][minute] == -1:
			pass
		else:
			counter += len(hubway.data[year][month][day+1][hour][minute])
	return counter

def plot(year):
	"""
	Combines ridership and temperature data into a dictionary
	and plots the dictionary.
	"""

	#determines whether or not it is a leap year
	if year % 4 == 0:
		numDaysInMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	else:
		numDaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

	riders_vs_temp = {}

	#adds all hourly temperatures in given year to dictionary as keys with values of 0
	for m in range(1,13):
		for d in range(numDaysInMonth[m-1]):
			for h in range(0,24):
				if int(float(weather.data[year][m][d+1][h]['tempi'])) < -100:
					pass
				else:
					riders_vs_temp[weather.data[year][m][d+1][h]['tempi']] = 0

	#adds number of riders to associated temperature in the dictionary
	for month in range(1,13):
		for day in range(numDaysInMonth[month-1]):
			for hour in range(24):
				if int(float(weather.data[year][month][day+1][hour]['tempi'])) < -100:
					pass
				else:
					riders_vs_temp[weather.data[year][month][day+1][hour]['tempi']] += count_riders(year, month, day, hour)

	#plots data
	x = riders_vs_temp.keys()
	y = riders_vs_temp.values()

	fig1 = plt.figure(1)
	ax1 = fig1.add_subplot(1,1,1)
	ax1.scatter(x,y)
	ax1.set_title("No Smoothing")
	ax1.set_xlabel("Temperature (F)")
	ax1.set_ylabel("# of Riders")
	show()


def plot_1degree(year):
	"""
	Combines ridership and temperature data into a dictionary
	and plots the dictionary.

	Smooths out temperature data by converting all floats to ints
	"""

	#determines whether or not it is a leap year
	if year % 4 == 0:
		numDaysInMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	else:
		numDaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

	riders_vs_temp = {}

	#adds all hourly temperatures in given year to dictionary as keys with values of 0
	for m in range(1,13):
		for d in range(numDaysInMonth[m-1]):
			for h in range(0,24):
				if int(float(weather.data[year][m][d+1][h]['tempi'])) < -100:
					pass
				else:
					riders_vs_temp[int(float(weather.data[year][m][d+1][h]['tempi']))] = 0

	#adds number of riders to associated temperature in the dictionary
	for month in range(1,13):
		for day in range(numDaysInMonth[month-1]):
			for hour in range(24):
				if int(float(weather.data[year][month][day+1][hour]['tempi'])) < -100:
					pass
				else:
					riders_vs_temp[int(float(weather.data[year][month][day+1][hour]['tempi']))] += count_riders(year, month, day, hour)

	#plots data
	x = riders_vs_temp.keys()
	y = riders_vs_temp.values()
	fig2 = plt.figure(2)
	ax2 = fig2.add_subplot(1,1,1)
	ax2.scatter(x,y)
	ax2.set_title("Smoothing (1 Degree)")
	ax2.set_xlabel("Temperature (F)")
	ax2.set_ylabel("# of Riders")
	show()


def plot_5degree(year):
	"""
	Combines ridership and temperature data into a dictionary
	and plots the dictionary.

	Smooths out temperature data by only using 5 degree chunks of temperature
	"""

	#determines whether or not it is a leap year
	if year % 4 == 0:
		numDaysInMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	else:
		numDaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

	riders_vs_temp = {}

	#adds all hourly temperatures in given year to dictionary as keys with values of 0
	for m in range(1,13):
		for d in range(numDaysInMonth[m-1]):
			for h in range(0,24):
				if int(float(weather.data[year][m][d+1][h]['tempi'])) < -100:
					pass
				else:
					riders_vs_temp[int(float(weather.data[year][m][d+1][h]['tempi']))] = 0

	#adds number of riders to associated temperature in the dictionary
	for month in range(1,13):
		for day in range(numDaysInMonth[month-1]):
			for hour in range(24):
				if int(float(weather.data[year][month][day+1][hour]['tempi'])) < -100:
					pass
				else:
					riders_vs_temp[int(float(weather.data[year][month][day+1][hour]['tempi']))] += count_riders(year, month, day, hour)

	spaces = 29
	temps = linspace(-20, 120, num=spaces)
	smoothed_riders_vs_temp = {}

	for temp in temps:
		smoothed_riders_vs_temp[temp] = 0

	for temp in temps:
		for degrees in range(int(temp-5),int(temp)):
			try:
				smoothed_riders_vs_temp[temp] += riders_vs_temp[degrees]
			except KeyError:
				pass

	#plots data
	x = smoothed_riders_vs_temp.keys()
	y = smoothed_riders_vs_temp.values()
	fig3 = plt.figure(3)
	ax3 = fig3.add_subplot(1,1,1)
	ax3.scatter(x,y)
	ax3.set_title("Smoothing (5 Degree)")
	ax3.set_xlabel("Temperature (F)")
	ax3.set_ylabel("# of Riders")
	show()

plot(2011)
plot_1degree(2011)
plot_5degree(2011)