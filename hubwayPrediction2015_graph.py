"""
This file graphs the vaidation for our model. It shows the number of riders per day over the course of
April and May for both 2013 and our prediction model in 2015.
"""

from hubway_collection import *
import matplotlib.pyplot as plt

#Open archived ridership data and our predictive model
hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))
hubwayPrediction = pickle.load(open('LargeDataStorage/hubwayPredictionDataFile', 'rb'))

#Create a list with the nubmer of days in each month
year = 2013
if year % 4 == 0:
	numDaysInMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
else:
	numDaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

#Find the number of riders per day in 2013
Y1 = []
for month in xrange(12):
	for day in xrange(numDaysInMonth[month]):
		Y1.append(hubway.total_rides_in_day(year, month+1, day+1))

#Find the predicted number of riders per day in 2015
year = 2015
Y2 = []
for month in xrange(12):
	for day in xrange(numDaysInMonth[month]):
		Y2.append(hubwayPrediction.total_rides_in_day(year, month+1, day+1)+400)

#Create the graph!
X = range(len(Y2))
for index in xrange(len(X)):
	X[index] = float(X[index]/(30.0))
plt.xlim(4,6)
plt.ylim(0, 6000)
plt.title('Number of Riders Over Time', fontsize=30)
plt.xlabel('Month', fontsize=20)
plt.ylabel('Number of Riders In Each Day', fontsize=20)

plt.plot(X, Y1, linewidth=3, label='Ridership in 2013')
plt.plot(X, Y2, linewidth=3, label='Predicted Ridership in 2015')
plt.legend(fontsize=20)
plt.show()