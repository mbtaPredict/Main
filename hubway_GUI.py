from Tkinter import *
from hubway_collection import *
from weather_collection import *
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class UserInterface(Frame):
    """
    This class represents the graphical user interface.
    """

    def __init__(self, master=None):
        """
        Creates a blank GUI.
        """

        Frame.__init__(self, master)
        self.pack()
        self.createUI()


    def get_hourly_data(month, day):
        hourlyData = []
        for hour in xrange(0,23):
            forecast = get_imminent_temp_precip_snow_hour(year, month, day, hour)
            forecastedTemp = forecast[0]
            forcastedPrecip = forecast[1]
            forcastedSnow = forecast[2]
            hourlyData[hour] = ridershipModel.predict(np.array([month, day, hour, forecastedTemp, forcastedPrecip, forcastedSnow]))


    def get_temp(self):
        """
        When the user presses the 'Get Temp!' button this function is called. This function
        displays the forecasted temperature for that hour.
        """

        #Gather the requested date
        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())
        hour = int(self.hour.get())

        date = '%i/%i/%i @%i' %(month, day, year, hour)
        try:
            self.temp['text'] = '%i degrees on %s' %(get_imminent_temp(year, month, day, hour), date)
        except:
            self.temp['text'] = 'We only have forecast data for the next 10 days. Please input a valid date.'


    def get_ridership(self):
        """
        When the user presses the 'Predict!'' button this function is called. This function
        displays the predicted ridership data for that hour and displays a graph that shows
        the number of riders on each hour on the day the user requested.
        """

        #Gather the requested date
        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())
        hour = int(self.hour.get())
        date = '%i/%i/%i @%i' %(month, day, year, hour)

        #If we have archived data for that date, display it
        #Create a list of all predicted rides in this day
        if year in hubway.data.keys() and month in hubway.data[year].keys() and day in hubway.data[year][month].keys() and hour in hubway.data[year][month][day].keys():
            dayPrediction = []
            for hourIndex in xrange(24):
                dayPrediction.append(hubway.total_rides_in_hour(year, month, day, hourIndex))
            #Display the data from the database
            self.ridership['text'] = 'From Database: %i rides on %s' %(dayPrediction[hour], date)

        #If we don't have archived data, then attempt to predict the ridership
        #Create a list of all predicted rides in this day
        else:
            dayData = get_imminent_temp_precip_snow_day(year, month, day)
            dayPrediction = []
            for hourIndex in xrange(len(dayData)):
                numRidesInHour = float(ridershipModel.predict(np.array([month, day, hourIndex, dayData[hourIndex][0], dayData[hourIndex][1], dayData[hourIndex][2]])))
                if numRidesInHour < 0:
                    numRidesInHour = 0
                dayPrediction.append(numRidesInHour)
            #Display the predicted ridership
            try:
                self.ridership['text'] = 'Prediction: %i rides on %s' %(dayPrediction[hour], date)
            #If the prediction date is not within the next 10 days, display an error
            except:        
                self.ridership['text'] = 'There is only archived data for 2011, 2012, and 2013. There is only prediction data for the next 10 days. Please input a valid date.'
        
        #Update the rides vs. hour graph
        f = Figure(figsize=(4,4), dpi=100)
        a = f.add_subplot(111)
        a.plot(range(len(dayPrediction)), dayPrediction)
        a.set_title('# of Rides Throughout the Day')
        a.set_xlabel('Hour')
        a.set_ylabel('Number of Rides')
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().grid(column=3, row=0, rowspan=7)

    def createUI(self):
        """
        Creates and organizes all the elements of the user interface.
        """

        #Window title
        self.master.title('hubwayPredict')

        #Year Input
        self.yearLabel = Label(self, text='Year')
        self.yearLabel.grid(column=0, row=0)
        self.year = Entry(self)
        self.year.grid(column=1, row=0, columnspan=2)

        #Month Input
        self.monthLabel = Label(self, text='Month')
        self.monthLabel.grid(column=0, row=1)
        self.month = Entry(self)
        self.month.grid(column=1, row=1, columnspan=2)

        #Day Input
        self.dayLabel = Label(self, text='Day')
        self.dayLabel.grid(column=0, row=2)
        self.day = Entry(self)
        self.day.grid(column=1, row=2, columnspan=2)

        #Hour Input
        self.hourLabel = Label(self, text='Hour')
        self.hourLabel.grid(column=0, row=3)
        self.hour = Entry(self)
        self.hour.grid(column=1, row=3, columnspan=2)

        #Ridership Button
        self.getRidership = Button(self, text='Predict!', fg='green', command=self.get_ridership)
        self.getRidership.grid(column=1, row=4)

        #Prediction Message
        self.ridership = Message(self, text='Enter a date and press the "Predict!" button!', width=200)
        self.ridership.grid(column=1, row=5, columnspan=1)

        #Graph of day prediction
        f = Figure(figsize=(4,4), dpi=100)
        a = f.add_subplot(111)
        a.plot(range(24),range(24))
        a.set_title('Input a Time!')
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().grid(column=3, row=0, rowspan=7)

        #Quit Button
        self.QUIT = Button(self, text='Quit', fg='red', width = 20, command=self.quit)
        self.QUIT.grid(column=1, row=6, columnspan=2)


if __name__ == '__main__':
    print 'Hubway data: loading...'
    hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))
    print 'Hubway data: complete'
    print 'Prediction model: loading...'
    ridershipModel = pickle.load(open('LargeDataStorage/mlModel', 'rb'))
    print 'Prediction model: complete'
    UI = UserInterface()
    UI.mainloop()