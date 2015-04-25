from hubway_collection import *
from weather_collection import *
import string

hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))
# weather = pickle.load(open('weatherDataFile', 'rb'))

print 'Welcome to hubwayPredict! Input any date and see what bike ridership will be like!'

def prediction():
	year = int(raw_input('Year: '))
	month = int(raw_input('Month: '))
	day = int(raw_input('Day: '))
	hourInput = raw_input('Do you want to specify an hour? ')
	if hourInput[0].lower() == 'y':
		hour = int(raw_input('Hour: '))
		if year in hubway.data.keys() and month in hubway.data[year].keys() and day in hubway.data[year][month].keys():
			print 'We seem to have that time on record. There were %i rides on %i/%i/%i at %i:00.' %(hubway.total_rides_in_hour(year, month, day, hour), month, day, year, hour)
		else:
			print 'We predict that %i rides will occur on %i/%i/%i at %i:00.' %(hubway.total_rides_in_hour(2013, month, day, hour)+(20*(year-2013)), month, day, year, hour)
	else:
		if year in hubway.data.keys() and month in hubway.data[year].keys() and day in hubway.data[year][month].keys():
			print 'We seem to have that date on record. There were %i rides on %i/%i/%i.' %(hubway.total_rides_in_day(year, month, day), month, day, year)
		else:
			print 'We predict that %i rides will occur on %i/%i/%i.' %(hubway.total_rides_in_day(2013, month, day)+(2000*(year-2013)), month, day, year)
	anotherPrediction = raw_input('Would you like to make another prediction? ')
	print '\n'

	#Does the user want to make more predictions?
	if anotherPrediction[0].lower() == 'y':
		prediction()
	else:
		print '\n Thanks for using hubwayPredict!'


if __name__ == '__main__':
	prediction()