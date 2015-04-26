from os import path
import csv
import pickle


def parse_datetime(datetime):
	"""
	Input: string of the format 4/2/2013 06:58:00
	Output: tuple of datetime (m,d,y,h,m,s)
	"""

	#splits date and time from datetime
	date = datetime.split(" ")[0]
	time = datetime.split(" ")[1]

	#splits date into m,d,y
	month = date.split("/")[0]
	day = date.split("/")[1]
	year = date.split("/")[2]

	#splits time into h,m,s
	hour = time.split(":")[0]
	minute = time.split(":")[1]
	second = time.split(":")[2]

	return year,month,day,hour,minute,second


def load_trips(year):
	"""
	Input: Year in which you want to return stored Hubway data.
	Output: List of dictionaries, where each dict contains the
			data for one Hubway trip
	"""

	year = str(year)

	data = []
	file_path = path.relpath("HubwayData/%s_hubway_trips.csv") % year
	
	#loads data from csv as a list of dictionaries
	with open(file_path) as f:
		reader = csv.DictReader(f)
		for row in reader:
			data.append(row)

	timestampedData = {}

	#Creates a dictionary of each data point with their start time being the key
	for dataPoint in data:
		if dataPoint['start_date'] in timestampedData:
			timestampedData[dataPoint['start_date']].append(dataPoint)
		else:
			timestampedData[dataPoint['start_date']] = [dataPoint]

	return timestampedData


def archived_minute(dataSet, year, month, day, hour, minute):
	"""
	Input: a dataset and specific minute
	Output: a list of ride details at that minute or -1 if no ride during that minute
	"""

	year = str(year)
	month = str(month)
	day = str(day)

	#Converts hour and minute into 2 digit integers (that are strings)
	hour = "%02d" % hour
	minute = "%02d" % minute

	timeStamp = month+'/'+day+'/'+year+' '+hour+':'+minute+':'+'00'

	if timeStamp in dataSet:
		return dataSet[timeStamp]
	else:
		return -1


class HubwayDatum:
	def __init__(self):
		self.data = {}

	def add_year(self, year):
		"""
		Input: integer for year you want to add hubway data for(we have to
			have the hubway data already stored for that year)
		Output: stores the hubway data for that year in the class
		"""

		yearHubwayData = load_trips(str(year))

		year = int(year)

		if year % 4 == 0:
			numDaysInMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		else:
			numDaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		self.data[year] = {}
		for month in xrange(12):
			self.data[year][month+1] = {}
			for day in xrange(numDaysInMonth[month]):
				self.data[year][month+1][day+1] = {}
				for hour in xrange(24):
					self.data[year][month+1][day+1][hour] = {}
					for minute in xrange(60):
						self.data[year][month+1][day+1][hour][minute] = archived_minute(yearHubwayData, year, month+1, day+1, hour, minute)

	def total_rides_in_day(self, year, month, day):
		"""
		Input: integers for year, month, day
		Return: integer for total number of rides on that day
		"""

		numRidesInDay = 0

		for hour in self.data[year][month][day]:
			for minute in self.data[year][month][day][hour]:
				if self.data[year][month][day][hour][minute] == -1:
					pass
				else:	
					numRidesInDay += len(self.data[year][month][day][hour][minute])
		return numRidesInDay

	def total_rides_in_hour(self, year, month, day, hour):
		"""
		Input: integers for year, month, day, hour
		Return: integer for total number of rides in that hour
		"""
		
		numRidesInHour = 0

		for minute in self.data[year][month][day][hour]:
			if self.data[year][month][day][hour][minute] == -1:
				pass
			else:	
				numRidesInHour += len(self.data[year][month][day][hour][minute])
		return numRidesInHour

# RUN THIS TO CREATE HUBWAY DATABASE CLASS STRUCTURE:
# ----------------------------------------------------
# hubway = HubwayDatum()
# hubway.add_year(2011)
# hubway.add_year(2012)
# hubway.add_year(2013)
# pickle.dump(hubway, open('LargeDataStorage/hubwayDataFile', 'wb'))
# ----------------------------------------------------

# RUN THIS TO OPEN THE HUBWAY DATABASE CLASS STRUCTURE:
# ----------------------------------------------------
# hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))
# ----------------------------------------------------