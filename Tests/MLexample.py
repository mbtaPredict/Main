import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import pickle
from hubway_collection import *
from weather_collection import *

hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))
weather = pickle.load(open('weatherDataFile', 'rb'))

# print weather.data[2013][4][1]

def average_day_temp(year, month, day):
	totalTemp = 0.0

	for hour in weather.data[year][month][day]:
		totalTemp += float(weather.data[year][month][day][hour]['tempi'])

	averageDayTemp = float(totalTemp) / len(weather.data[year][month][day])
	return averageDayTemp

###############################################################################
# Generate sample data
X = []
y = []

for day in xrange(29):
	X.append([average_day_temp(2013, 4, day+1)])
	y.append(hubway.total_rides_in_day(2013, 4, day+1))

print 'Temp:', X
print 'Number of Rides:', y

###############################################################################
# Add noise to targets
# y[::5] += 3 * (0.5 - np.random.rand(8))

###############################################################################
# Fit regression model
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(X, y).predict(X)
y_lin = svr_lin.fit(X, y).predict(X)
y_poly = svr_poly.fit(X, y).predict(X)

###############################################################################
# look at the results
plt.scatter(X, y, c='k', label='data')
plt.hold('on')
plt.plot(X, y_rbf, c='g', label='RBF model')
plt.plot(X, y_lin, c='r', label='Linear model')
plt.plot(X, y_poly, c='b', label='Polynomial model')
plt.xlabel('data')
plt.ylabel('target')
plt.title('Support Vector Regression')
plt.legend()
plt.show()