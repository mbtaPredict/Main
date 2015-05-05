"""
This is the setup file that must be run before using hubwayPredict. The weather data is optional,
but the hubway data must be stored in order to run our program.
"""

from weather_collection import *
from hubway_collection import *
import pickle

#Creates the weather data class structure.
#NOTE: this takes a long time to generate
#Only run this if you want the data for analysis or machine learning purposes
# ----------------------------------------------------------------------
# weather = WeatherDatum()
# weather.add_year(2011)
# weather.add_year(2012)
# weather.add_year(2013)
# weather.add_year(2014)
# pickle.dump(weather, open('LargeDataStorage/weatherDataFile', 'wb'))
# ----------------------------------------------------------------------

#Creates the hubway ridership data class structure
# ----------------------------------------------------------------------
hubway = HubwayDatum()
hubway.add_year(2011)
hubway.add_year(2012)
hubway.add_year(2013)
pickle.dump(hubway, open('LargeDataStorage/hubwayDataFile', 'wb'))
# ----------------------------------------------------------------------