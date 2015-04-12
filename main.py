"""
Main file for hubwayPredict project.
"""

from os import path
import ast
import matplotlib.pyplot as plt
from hubway_data_parsing import load_trips

def plot_duration(year):
	"""
	Plots duration of hubway rides in a bar chart.
	Input: year of data that gets graphed
	Output: bar chart of data
	"""
	
	data = load_trips(year)

	#creates dictionary counting frequency of each trip duration
	durations = {}
	for d in data:
		if d['duration'] not in durations:
			durations[d['duration']] = 1
		else:
			durations[d['duration']] += 1

	return durations

if __name__ == "__main__":
	print plot_duration(2013)