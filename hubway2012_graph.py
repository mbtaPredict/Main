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

def fourierExtrapolation(x, n_predict):
    n = x.size
    n_harm = 4                     # number of harmonics in model
    t = np.arange(0, n)
    p = np.polyfit(t, x, 1)  # find linear trend in x
    x_notrend = x - p[0] * t # detrended x
    x_freqdom = fft.fft(x_notrend)  # detrended x in frequency domain
    f = fft.fftfreq(n)              # frequencies
    indexes = range(n)
    # sort indexes by frequency, lower -> higher
    indexes.sort(key = lambda i: np.absolute(f[i]))
 
    t = np.arange(0, n + n_predict)
    restored_sig = np.zeros(t.size)
    for i in indexes[:1 + n_harm * 2]:
        ampli = np.absolute(x_freqdom[i]) / n   # amplitude
        phase = np.angle(x_freqdom[i])          # phase
        restored_sig += ampli * np.cos(2 * np.pi * f[i] * t + phase)
    return restored_sig + p[0] * t

def day_of_week_classifier(data):
 	#Hubway opened on March 13th, a Tuesday, in 2012
 	tues_start = 0
 	wed_start = 1
 	thurs_start = 2
 	fri_start = 3
 	sat_start = 4
 	sun_start = 5
 	mon_start = 6

 	mon = data[mon_start::7]
 	tues = data[tues_start::7]
 	wed = data[wed_start::7]
 	thurs = data[thurs_start::7]
 	fri = data[fri_start::7]
 	sat = data[sat_start::7]
 	sun = data[sun_start::7]

 	return (mon, tues, wed, thurs, fri, sat, sun)

def sum_daily_totals(daily_totals):
	mon_sum = sum(daily_totals[0])
	tues_sum = sum(daily_totals[1])
	wed_sum = sum(daily_totals[2])
	thurs_sum = sum(daily_totals[3])
	fri_sum = sum(daily_totals[4])
	sat_sum = sum(daily_totals[5])
	sun_sum = sum(daily_totals[6])

	return (mon_sum, tues_sum, wed_sum, thurs_sum, fri_sum, sat_sum, sun_sum)

def average_daily_totals(daily_totals):
	mon_ave = sum(daily_totals[0])/len(daily_totals[0])
	tues_ave = sum(daily_totals[1])/len(daily_totals[1])
	wed_ave = sum(daily_totals[2])/len(daily_totals[2])
	thurs_ave = sum(daily_totals[3])/len(daily_totals[3])
	fri_ave = sum(daily_totals[4])/len(daily_totals[4])
	sat_ave = sum(daily_totals[5])/len(daily_totals[5])
	sun_ave = sum(daily_totals[6])/len(daily_totals[6])

	return (mon_ave, tues_ave, wed_ave, thurs_ave, fri_ave, sat_ave, sun_ave)

def main(): 
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
	march_count = march_count[12:]

	april_count = []

	for x in range(1,32):
		april_count.append(april.count(str(x)))
	april_count = april_count[:-1]

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

	#polynomial regression
	fig1 = plt.figure(1)
	yreg = all_months_count
	xreg = range(len(yreg)) #each day counts up by 1
	fit = polyfit(xreg,yreg,4) #regression
	fit_fn = poly1d(fit) #generate polynomial from regression function
	ax1 = fig1.add_subplot(111)
	ax1.plot(xreg,yreg,'yo', xreg, fit_fn(xreg), '--k') #plot regression

	#regular line plot
	#plt.plot(all_months_count) 

	#Fourier Transform Regression
	"""
	xfour = np.array(yreg[70:70+21])
	n_predict = len(xreg[70:70+21])
	extrapolation = fourierExtrapolation(xfour, n_predict)
	plt.plot(np.arange(0, extrapolation.size), extrapolation, 'r', label = 'extrapolation')
	plt.plot(np.arange(0, xfour.size), xfour, 'b', label = 'x', linewidth = 3)
	plt.plot(xreg[21:21+21],all_months_count[70+21:70+21+21])
	plt.legend()
	plt.show()
	"""


	ax1.set_xlabel('Day of Operation')
	ax1.set_ylabel('Number of Riders')
	ax1.set_title('Hubway Ridership in 2012')

	daily_totals = day_of_week_classifier(all_months_count)
	sum_totals = sum_daily_totals(daily_totals)

	fig2 = plt.figure(2)
	ax2 = fig2.add_subplot(111)
	ax2.bar(range(7),sum_totals, 1/1.5, color = "blue")
	ax2.set_xlabel('Day of Week')
	ax2.set_ylabel('Amount of Riders')
	ax2.set_title('Total Ridership by Day')

	ave_totals = average_daily_totals(daily_totals)

	fig3 = plt.figure(3)
	ax3 = fig3.add_subplot(111)
	ax3.bar(range(7),ave_totals, 1/1.5, color = "blue")
	ax3.set_xlabel('Day of Week')
	ax3.set_ylabel('Amount of Riders')
	ax3.set_title('Average Ridership by Day')

	fig4 = plt.figure(4)
	ax4 = fig4.add_subplot(111)
	ax4.bar(range(len(daily_totals[0])),daily_totals[0], 1/1.5, color = "blue")
	ax4.set_xlabel('Time of Year')
	ax4.set_ylabel('Amount of Riders')
	ax4.set_title('Average Ridership for Mondays')
	
	show()

if __name__ == "__main__":
    main()