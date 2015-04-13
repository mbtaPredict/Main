"""
Main file for hubwayPredict project.
"""

from os import path
import ast
import matplotlib.pyplot as plt
from hubway_data_parsing import load_trips
import numpy as np
from collections import OrderedDict

def plot_duration(year):
	"""
	Plots duration of hubway rides in a bar chart.
	Input: year of data that gets graphed
	Output: bar chart of data
	"""
	
	data = load_trips(year)

	#creates dictionary counting frequency of each trip duration
	durations = OrderedDict()
	for d in data:
		if d['duration'] not in durations:
			durations[d['duration']] = 1
		else:
			durations[d['duration']] += 1

	print durations

	N = len(durations)
	column_height = list(durations.iterkeys())

	for item in range(len(column_height)):
		column_height[item] = int(column_height[item])
	column_height = tuple(column_height)

	print column_height

	ind = np.arange(N) #the x locations for the groups
	width = 0.1		   #the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, column_height, width)

	ax.set_ylabel('Number of Rides')
	ax.set_title('Duration of Hubway Rides')
	ax.set_xlabel('Ride Duration')

	plt.show()

if __name__ == "__main__":
	plot_duration(2013)