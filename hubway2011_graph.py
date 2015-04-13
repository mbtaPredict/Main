"""Part of Hubway Prediction project by Shane Kelly, William Lu, and
Kevin Crispie, Olin College of Engineering
"""

import csv
import matplotlib.pyplot as plt
import matplotlib
from pylab import *


def get_file(file_path):
	""" reads a csv file and returns a file file_id
	"""

	f = open(file_path, 'r')
	bike_reader = csv.reader(f)

	return bike_reader


def get_month_days(file_id):
	"""takes a file id and returns month_days, a list of all the individual 
	Hubway trips in a month in a list of lists. Each nested list has all the 
	dates for each trip in the given month_days
	"""

	standard_datetime = []
	for line in file_id:
		standard_datetime.append(line[4]) #append the contents of line 4 (trip start date)

	standard_datetime = standard_datetime [1::]	#removes header text from list

	month = []
	day = []
	year = []

	#creates lists of trip months, days, and years, multiplicty is number of trips during 
	#that time period

	for i in range(len(standard_datetime)):
		only_date = standard_datetime[i].split(' ')
		only_date_string = only_date[0]
		split_date_string = only_date_string.split('/')
		month.append(split_date_string[0])
		day.append(split_date_string[1])
		year.append(split_date_string[2])
	


	#separates a large list of days into corresponding month
	july = day[0:month.index('8')]
	august = day[month.index('8'):month.index('9')]
	september = day[month.index('9'):month.index('10')]
	october = day[month.index('10'):month.index('11')]
	november = day[month.index('11')::]

	return [july, august, september, october, november]


file_path = 'HubwayData/2011_hubway_trips.csv'
bike_reader = get_file(file_path)
month_days = get_month_days(bike_reader)

#list corresping to date of trips for each month
july = month_days[0]
august = month_days[1]
september = month_days[2]
october = month_days[3]
november = month_days[4]

#counts the number of trips in each month

july_count = []

for x in range(1,32):
	july_count.append(july.count(str(x)))
july_count = july_count[27:]

august_count = []

for x in range(1,32):
	august_count.append(august.count(str(x)))

september_count = []

for x in range(1,32):
	september_count.append(september.count(str(x)))
september_count = september_count[:-1]

october_count = []

for x in range(1,32):
	october_count.append(october.count(str(x)))

november_count = []

for x in range(1,32):
	november_count.append(november.count(str(x)))
november_count = november_count[:-1]

#get a list of number of trips for all months
all_months_count = july_count + august_count + september_count + october_count + november_count
y = all_months_count
x = range(len(y)) #each day counts up by 1
fit = polyfit(x,y,4) #regression
fit_fn = poly1d(fit) #generate polynomial from regression function
plot(x,y,'yo', x, fit_fn(x), '--k') #plot regression
#plt.plot(all_months_count) #regular line plot
plt.xlabel('Day of Operation')
plt.ylabel('Number of Riders')
plt.title('Hubway Ridership in 2011')
plt.show()