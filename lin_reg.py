"""
/hubwayPredict by William Lu, Shane Kelly, and Kevin Crispie
lin_reg.py generates a 7 degree polynomial ridge regression model for hubway ridership
Output: File stored in /LargeDataStorage/mlModel containing pickled ridership model
"""
from datetime import date
import pickle
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


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
		if hubway.data[year][month][day][hour][minute] == -1:
			pass
		else:
			counter += len(hubway.data[year][month][day][hour][minute])
	return counter


def process_data():
    """
    Output: Array formatted like array([year, month, day, hour, temp, precip, snow, riders])
    Warning: hard-coded for hubway data from 2013
    Note: snow data is binary, units are in imperial (english) units

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

        # create list of data that is then appended to all_data list, which becomes a list of lists
        for month in range(4, 6):
            for day in range(numDaysInMonth[month-4]):
                for hour in range(0,24):
                    # this is here to make sure that data for April starts on the 2nd
                    if month == 4:
                        weekday = int(date(year, month, day+2).weekday()<5)
                        tempi = int(float(weather.data[year][month][day+2][hour]['tempi']))
                        if int(float(weather.data[year][month][day+2][hour]['precipi'])) < 0:
                            precipi = 0
                        else: 
                            precipi = int(float(weather.data[year][month][day+2][hour]['precipi']))
                        snow = int(weather.data[year][month][day+2][hour]['snow'])
                        riders = count_riders(year, month, day+2, hour)
                        #Depending on what model you are creating, use different 'curr_list'
                        # curr_list = [year, month, day+2, hour, weekday, tempi, precipi, snow, riders]
                        curr_list = [year, month, day+2, hour, riders]
                        all_data.append(curr_list)
                    else:
                        weekday = int(date(year, month, day+1).weekday()<5)
                        tempi = int(float(weather.data[year][month][day+1][hour]['tempi']))
                        if int(float(weather.data[year][month][day+1][hour]['precipi'])) < 0:
                            precipi = 0
                        else:
                            precipi = int(float(weather.data[year][month][day+1][hour]['precipi']))
                        snow = int(weather.data[year][month][day+1][hour]['snow'])
                        riders = count_riders(year, month, day+1, hour)
                        #Depending on what model you are creating, use different 'curr_list'
                        # curr_list = [year, month, day+1, hour, weekday, tempi, precipi, snow, riders]
                        curr_list = [year, month, day+1, hour, riders]
                        all_data.append(curr_list)
    
    # transforms all_data into an array and returns it
    return np.array(all_data)


def lin_reg():
    """
    Creates and saves ridge regression model for hubway ridership.
    """
    
    year = 2013
    
    # import temperature and ridership data
    data_array = process_data()
    
    # select month, day, hour, temperature, precipitation, and snow data from data_array
    X = data_array[:,[1,2,3]]
    # select ridership data from data_array
    Y = data_array[:,4]

    # make array vertical so that scikit-learn can process it
    X = X.reshape(X.shape[0], -1)
    Y = Y.reshape(Y.shape[0], -1)

    # splits data into training and testing bits
    X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.5)
    
    # sets degree of polynomial regression
    # in testing, anything greater than 7 will give a MemoryError
    degrees = 7

    # initalize scikit-learn model
    model = make_pipeline(PolynomialFeatures(degrees), Ridge())

    # fits a model to training data
    print 'fitting model...'
    model.fit(X_train, y_train)

    # scores model
    print "Year %d, %d degree polynomial regression" % (year, degrees)
    print "Train R^2 %f"%model.score(X_train, y_train)
    print "Test R^2 %f"%model.score(X_test, y_test)

    # pickles and saves model
    pickle.dump(model, open('LargeDataStorage/mlModelNoWeather', 'wb'))
    pass

if __name__ == '__main__':
    #load weather data
    print 'loading weather...'
    from weather_collection import WeatherDatum
    weather = pickle.load(open('LargeDataStorage/weatherDataFile', 'rb'))

    #load hubway data
    print 'loading ridership...'
    from hubway_collection import HubwayDatum
    hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))
    lin_reg()