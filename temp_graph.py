from pprint import pprint
from os import path
import ast
import matplotlib.pyplot as plt
from pylab import *
from weather_collection import archived_day
from weather_collection import archived_hour

def parse_weather(month, day, year):
	"""
	Input: month, day, and year for the day you wish to pull weather data
	"""

	#converts day and month into 2 digit integers with leading zeros
	day = "%02d" % day
	month = "%02d" % month

	#establishes file path for txt file
	file_path = path.relpath("%sData/%s-%s-%s.txt") % (year, year, month, day)

	f = open(file_path, 'r')
	weatherData = f.read()
	weatherData = ast.literal_eval(weatherData)
	return weatherData

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

	#calls parse_weather for each day of the year and appends temperature for
	#each hour into the all_temps list
	all_temps = []
	for month in range(4,12):
		for day in month_days[month]:
			for hour in range(24):
				#converts month, day, and hour into 2 digit integers with leading zeros
				#for input into archived_hour
				year = str(year)
				month = int(month)
				day = int(day)
				hour = int(hour)
				month = "%02d" % month
				day = "%02d" % day
				hour = "%02d" % hour

				weatherData = archived_hour(year, month, day, hour)
				all_temps.append(weatherData['tempi'])

	#converts all strings in all_temps into floats
	for i in range(len(all_temps)):
		all_temps[i] = float(all_temps[i])

	x = range(len(all_temps)) #crea
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