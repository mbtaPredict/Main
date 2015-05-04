import pickle
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

print "loading data"
#load weather data
from weather_collection import WeatherDatum
weather = pickle.load(open('LargeDataStorage/weatherDataFile', 'rb'))

#load hubway data
hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))

def count_riders2(year, month, day, hour):
	"""
	Input: year, month, day, hour
	Output: total riders during that hour
	"""

	#initialize counter
	counter = 0

	#counts riders during a given hour
	for minute in range(0,60):
		#-1 means that there is no data for that time, so we don't count that
		if hubway.data[year][month][day][hour][minute] == -1:
			pass
		else:
			counter += len(hubway.data[year][month][day][hour][minute])
	return counter

def process_data2():
    """
    Warning: hard-coded for hubway data from 2013
    Output: Array formatted array([year, month, day, hour, temp, precip, snow*, riders])
    Note: * data is binary, units are in imperial (english) units
    """
    
    year = 2013
    
    # not a leap year, also taking into account dates hubway was open
    # 2013 start = 4/2/2013
    # 2013 end = 11/30/2013
    numDaysInMonth = [29, 31, 30, 31, 31, 30, 31, 30]
    
    # initalize main list for data
    all_data = []
    
    for index in range(sum(numDaysInMonth)):
        # initalize list that will be appended to all_data
        curr_list = [year]

        for month in range(4, 6):
            for day in range(numDaysInMonth[month-4]):
                for hour in range(0,24):
                    # this is here to make sure that data for April starts on the 2nd
                    if month == 4:
                        tempi = int(float(weather.data[year][month][day+2][hour]['tempi']))
                        if int(float(weather.data[year][month][day+2][hour]['precipi'])) < 0:
                            precipi = 0
                        else: 
                            precipi = int(float(weather.data[year][month][day+2][hour]['precipi']))
                        snow = int(weather.data[year][month][day+2][hour]['snow'])
                        riders = count_riders2(year, month, day+2, hour)
                        curr_list = [year, month, day+2, hour, tempi, precipi, snow, riders]
                        all_data.append(curr_list)
                    else:
                        tempi = int(float(weather.data[year][month][day+1][hour]['tempi']))
                        if int(float(weather.data[year][month][day+1][hour]['precipi'])) < 0:
                            precipi = 0
                        else:
                            precipi = int(float(weather.data[year][month][day+1][hour]['precipi']))
                        snow = int(weather.data[year][month][day+1][hour]['snow'])
                        riders = count_riders2(year, month, day+1, hour)
                        curr_list = [year, month, day+1, hour, tempi, precipi, snow, riders]
                        all_data.append(curr_list)
    
    return np.array(all_data)

def lin_reg():
    
    year = 2013
    
    print "processing data"
    # import temperature and ridership data
    data_array = process_data2()
    
    print "selecting data from array"
    X = data_array[:,[1,2,3,4,5,6]]
    Y = data_array[:,7]

    print "reshaping data"
    # make array vertical so that scikit-learn can process it
    X = X.reshape(X.shape[0], -1)
    Y = Y.reshape(Y.shape[0], -1)
    
    print "train test split"
    X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.5)
    
    degrees = 7

    print "making a pipeline"
    model = make_pipeline(PolynomialFeatures(degrees), Ridge())

    print "fitting model"
    model.fit(X_train, y_train)

    print "scoring model"
    print "Year %d, %d degree polynomial regression, month+day+hour" % (year, degrees)
    print "Train R2 %f"%model.score(X_train, y_train)
    print "Test R2 %f"%model.score(X_test, y_test)

    print "pickle dumping"
    pickle.dump(model, open('LargeDataStorage/mlModel8', 'wb'))
    print "done dumping"
#         y_plot = model.predict(X)
#         plt.plot(X, y_plot)
#         plt.show()
    
    return

lin_reg()