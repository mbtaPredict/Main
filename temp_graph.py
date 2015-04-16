from pprint import pprint
from os import path
import ast
import matplotlib.pyplot as plt
from pylab import *
import pickle

from weather_collection import WeatherDatum

weather = pickle.load(open('weatherDataFile', 'rb'))

def plot_weather(year):
	"""
	Input: Year in which you want to graph data.
	Output: Graph of temperatures for the entire year.
	"""

	#establish number of days for long and short months
	long_month_days = range(1, 32)
	short_month_days = range(1, 31)
	february_days = range(1, 29)
	feburary_leap_days = range(1, 30)

	#checks if the inputted year is a leap year and then assigns days to months
	if year % 4 == 0:
		month_days = {1:long_month_days, 2:february_leap_days, 3:long_month_days,
						4:short_month_days, 5:long_month_days, 6:short_month_days,
						7:long_month_days, 8:long_month_days, 9:short_month_days,
						10:long_month_days, 11:short_month_days, 12:long_month_days}
	else:
		month_days = {1:long_month_days, 2:february_days, 3:long_month_days,
						4:short_month_days, 5:long_month_days, 6:short_month_days,
						7:long_month_days, 8:long_month_days, 9:short_month_days,
						10:long_month_days, 11:short_month_days, 12:long_month_days}

	#appends temperature for each hour into the all_temps list
	all_temps = []
	for month in range(4,12):
		for day in month_days[month]:
			for hour in range(24):
				all_temps.append(weather.data[year][month][day][hour]['tempi'])

	#converts all strings in all_temps into floats
	for i in range(len(all_temps)):
		all_temps[i] = float(all_temps[i])

	x = range(len(all_temps)) #create x axis
	fit = polyfit(x,all_temps,3) #generate regression with number as degree
	fit_fn = poly1d(fit) #create polynomial to graph
	plot(x,all_temps, x, fit_fn(x), '--k') #plot regression

	#plots all_temps
	plot_title = "Hourly Temperatures in %s" % year + " (April 1st - November 30th)"
	# plt.plot(all_temps)
	plt.xlabel('Hour')
	plt.ylabel('Temperature (degrees F)')
	plt.title(plot_title)
	plt.show()


if __name__ == "__main__":
	plot_weather(2013)