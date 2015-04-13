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
	f = open(file_path, 'r') #open with read
	bike_reader = csv.reader(f)

	return bike_reader


def get_month_days(file_id):
	"""takes a file id and returns month_days, a list of all the individual 
	Hubway trips in a month in a list of lists. Each nested list has all the 
	dates for each trip in the given month_days
	"""
	standard_datetime = []
	for line in file_id:
		standard_datetime.append(line[4]) #appends trip start date to list

	standard_datetime = standard_datetime [1::]	#removes header text from list

	month = []
	day = []
	year = []

	#creates lists of trip months, days, and years, multiplicty is number of trips during 
	#that time period

	for i in range(len(standard_datetime)):
		only_date = standard_datetime[i].split(' ')
		only_date_string = only_date[0]
		split_date_string = only_date_string.split('/') #separate out parts of date
		month.append(split_date_string[0])
		day.append(split_date_string[1])
		year.append(split_date_string[2])
	#print day

	march = day[month.index('3'):month.index('4')]
	april = day[month.index('4'):month.index('5')]
	may = day[month.index('5'):month.index('6')]
	june = day[month.index('6'):month.index('7')]
	july = day[month.index('7'):month.index('8')]
	august = day[month.index('8'):month.index('9')]
	september = day[month.index('9'):month.index('10')]
	october = day[month.index('10'):month.index('11')]
	november = day[month.index('11')::]

	return [march, april, may,  june, july, august, september, october, november]


file_path = 'HubwayData/2012_hubway_trips.csv'
bike_reader = get_file(file_path)
month_days = get_month_days(bike_reader)

#separate out trips by month

march = month_days[0]
april = month_days[1]
may = month_days[2]
june = month_days[3]
july = month_days[4]
august = month_days[5]
september = month_days[6]
october = month_days[7]
november = month_days[8]

#count number of trips for each day, separated by month

march_count = []

for x in range(1,32):
	march_count.append(march.count(str(x)))
march_count = march_count[14:]


april_count = []

for x in range(1,32):
	april_count.append(april.count(str(x)))
april_count = april_count(:-1)

may_count = []

for x in range(1,32):
	may_count.append(may.count(str(x)))

june_count = []

for x in range(1,32):
	june_count.append(june.count(str(x)))
june_count = june_count[:-1]

july_count = []

for x in range(1,32):
	july_count.append(july.count(str(x)))

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
november_count = november_count[:-3]

#get a list of number of trips for each month
all_months_count = march_count + april_count + may_count + june_count + july_count + august_count + september_count + october_count + november_count

y = all_months_count
x = range(len(y)) #increases 1 per day
fit = polyfit(x,y,3) #generate regression with number as degree
fit_fn = poly1d(fit) #create polynomial to graph
plot(x,y,'yo', x, fit_fn(x), '--k') #plot regression
#plt.plot(all_months_count) #regular line plot
plt.xlabel('Day of Operation')
plt.ylabel('Number of Riders')
plt.title('Hubway Ridership in 2012')
plt.show()