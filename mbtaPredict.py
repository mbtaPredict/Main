import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json

WUNDERGROUND_API_KEY = "3ec21efc1c37b8b2"
WUNDERGROUND_BASE_URL = "http://api.wunderground.com/api/"+WUNDERGROUND_API_KEY


def json(url):
	f = f = urllib2.urlopen(url)
	return f.read()


def weather_on(date):
	return json(WUNDERGROUND_BASE_URL+ "/history_" + date + "/q/MA/Boston.json")

def store_2014_data():
	year = 2014
	month = 1
	day = 1
	month31 = [1, 3, 5, 7, 8, 10, 12]
	month30 = [4, 6, 9, 11]
	month28 = [2]
	number = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
			'16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
	for x in xrange(365):
		for x in range(12):
			day = 1
			if month in month31:
				for x in range(31):
					date = str(year)+number[month]+number[day]
					f = open(str(year)+'Data/'+str(year)+'-'+number[month]+'-'+number[day]+'.txt', 'w')
					f.write(weather_on(date))
					f.close()
					day += 1
			elif month in month30:
				for x in range(30):
					date = str(year)+number[month]+number[day]
					f = open(str(year)+'Data/'+str(year)+'-'+number[month]+'-'+number[day]+'.txt', 'w')
					f.write(weather_on(date))
					f.close()
					day += 1
			elif month in month28:
				for x in range(28):
					date = str(year)+number[month]+number[day]
					f = open(str(year)+'Data/'+str(year)+'-'+number[month]+'-'+number[day]+'.txt', 'w')
					f.write(weather_on(date))
					f.close()
					day += 1
			month += 1
store_2014_data()