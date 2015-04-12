from os import path
import csv

def load_trips(year):
	"""
	Input: Year in which you want to return stored Hubway data.
	Output: Text file with a list of dictionaries, where each
			dict contains the data for one Hubway trip
	Text file name: YYYY_hubway_trips.txt
	"""
	data = []
	file_path = path.relpath("HubwayData/%s_hubway_trips.csv") % year
	
	#loads data from csv as a list of dictionaries
	with open(file_path) as f:
		reader = csv.DictReader(f)
		for row in reader:
			data.append(row)

	new_file_path = path.relpath("HubwayData/%s_hubway_trips.txt") % year

	#saves list of dictionaries into txt file
	f = open(new_file_path, 'a')
	f.write(str(data))
	f.close()

if __name__ == "__main__":
    load_trips(2013)