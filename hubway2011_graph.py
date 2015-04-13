import csv
import matplotlib.pyplot as plt
import matplotlib
from pylab import *

def get_file(file_path):
	f = open(file_path, 'r')
	bike_reader = csv.reader(f)

	return bike_reader

def get_month_days(file_id):
	standard_datetime = []
	for line in file_id:
		standard_datetime.append(line[4])

	standard_datetime = standard_datetime [1::]	

	month = []
	day = []
	year = []

	for i in range(len(standard_datetime)):
		only_date = standard_datetime[i].split(' ')
		only_date_string = only_date[0]
		split_date_string = only_date_string.split('/')
		month.append(split_date_string[0])
		day.append(split_date_string[1])
		year.append(split_date_string[2])
	#print day

	july = day[0:month.index('8')]
	august = day[month.index('8'):month.index('9')]
	september = day[month.index('9'):month.index('10')]
	october = day[month.index('10'):month.index('11')]
	november = day[month.index('11')::]

	return [july, august, september, october, november]


file_path = 'HubwayData/2011_hubway_trips.csv'
bike_reader = get_file(file_path)
month_days = get_month_days(bike_reader)
july = month_days[0]
august = month_days[1]
september = month_days[2]
october = month_days[3]
november = month_days[4]


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

all_months_count = july_count + august_count + september_count + october_count + november_count
y = all_months_count
x = range(len(y))
fit = polyfit(x,y,5)
fit_fn = poly1d(fit)
#plot(x,y,'yo', x, fit_fn(x), '--k')

print len(all_months_count)
print all_months_count

plt.plot(all_months_count)
plt.xlabel('Day of Operation')
plt.ylabel('Number of Riders')
plt.title('Hubway Ridership in 2011')
plt.show()