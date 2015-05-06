from Tkinter import *
from datetime import *
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


    def get_ridership(self):
        """
        When the user presses the 'Predict!'' button this function is called. This function
        displays the predicted/archived ridership data for that hour and displays a graph that shows
        the number of riders on each hour on the day the user requested.
        """

        #Gather the requested date
        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())
        hour = int(self.hour.get())
        prettyDate = '%i/%i/%i @%i' %(month, day, year, hour)

        try:
            currentDate = datetime(year, month, day, hour, 0, 0)
        except:
            self.ridership['text'] = 'Please input a valid date.'
            return
        #If we have archived data for that date, display it
        #Create a list of all predicted rides in this day
        if year in hubway.data.keys() and month in hubway.data[year].keys() and day in hubway.data[year][month].keys() and hour in hubway.data[year][month][day].keys():
            dayPrediction = []
            for hourIndex in xrange(24):
                dayPrediction.append(hubway.total_rides_in_hour(year, month, day, hourIndex))
            #Display the data from the database
            self.ridership['text'] = 'From Database: %i rides on %s' %(dayPrediction[hour], prettyDate)

        #If the requested date is today, then display the predicted ridership with a more accurate model
        elif (date(year, month, day)-date.today()).days==0:
            dayData = get_imminent_weekday_temp_precip_snow_day(year, month, day)
            dayPrediction = []
            for hourIndex in xrange(len(dayData)):
                numRidesInHour = float(ridershipModelImminent.predict(np.array([month, day, hourIndex, dayData[hourIndex][1], dayData[hourIndex][2], dayData[hourIndex][3]])))
                if numRidesInHour < 0:
                    numRidesInHour = 0
                if numRidesInHour > 600:
                    numRidesInHour = 600
                dayPrediction.append(numRidesInHour)
            #Display the predicted ridership
            print dayPrediction
            self.ridership['text'] = "Today's Prediction, %s, look to the graph!" %prettyDate

        #If the requested date is within the next 240 hours, then display the predicted ridership with a more accurate model
        elif (date(year, month, day)-date.today()).days<10 and (date(year, month, day)-date.today()).days>0:
            dayData = get_imminent_weekday_temp_precip_snow_day(year, month, day)
            dayPrediction = []
            for hourIndex in xrange(len(dayData)):
                numRidesInHour = float(ridershipModelImminent.predict(np.array([month, day, hourIndex, dayData[hourIndex][1], dayData[hourIndex][2], dayData[hourIndex][3]])))
                if numRidesInHour < 0:
                    numRidesInHour = 0
                dayPrediction.append(numRidesInHour)
            #Display the predicted ridership
            self.ridership['text'] = 'Imminent Prediction: %i rides on %s' %(dayPrediction[hour], prettyDate)
        
        #If the requested date is past the next 240 hours, then display the predicted ridership with a less accurate model
        elif (date(year, month, day)-date.today()).days>=10 and year==2015:
            dayPrediction = []
            for hourIndex in xrange(24):
                numRidesInHour = float(ridershipModelFar.predict(np.array([month, day, hourIndex])))
                if numRidesInHour < 0:
                    numRidesInHour = 0
                if numRidesInHour > 600:
                    numRidesInHour = 600
                dayPrediction.append(numRidesInHour)
            #Display the predicted ridership
            self.ridership['text'] = 'Distant Prediction: %i rides on %s' %(dayPrediction[hour], prettyDate)
        
        #If the requested date somehow slips through, display an error.
        else:
            self.ridership['text'] = 'There is only archived data for 2011, 2012, and 2013. There is only prediction data from today until the end of 2015. Please input a valid date.'
            return
        #Update the rides vs. hour graph
        f = Figure(figsize=(4,4), dpi=100)
        a = f.add_subplot(111)
        dayPrediction = [0]*(24-len(dayPrediction)) + dayPrediction
        a.plot(range(24), dayPrediction)
        a.set_title('# of Rides Throughout the Day')
        a.set_xlabel('Hour')
        a.set_ylabel('Number of Rides')
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().grid(column=3, row=0, rowspan=8)



    def createUI(self):
        """
        Creates and organizes all the elements of the user interface.
        """

        #Window title
        self.master.title('hubwayPredict')

        #Instructions
        self.instructions = Message(self, text='Archived Data:\n   2011 - 8\n   2012 - 4, 5, 6, 7, 8, 9, 10\n   2013 - 4, 5, 6, 7, 8, 9, 10, 11\nPrediction Data:\n   2015 - today until end of May', width=200)
        self.instructions.grid(column=0, row=0, columnspan=2)
        #Year Input
        self.yearLabel = Label(self, text='Year')
        self.yearLabel.grid(column=0, row=1)
        self.year = Entry(self)
        self.year.grid(column=1, row=1, columnspan=2)

        #Month Input
        self.monthLabel = Label(self, text='Month')
        self.monthLabel.grid(column=0, row=2)
        self.month = Entry(self)
        self.month.grid(column=1, row=2, columnspan=2)

        #Day Input
        self.dayLabel = Label(self, text='Day')
        self.dayLabel.grid(column=0, row=3)
        self.day = Entry(self)
        self.day.grid(column=1, row=3, columnspan=2)

        #Hour Input
        self.hourLabel = Label(self, text='Hour')
        self.hourLabel.grid(column=0, row=4)
        self.hour = Entry(self)
        self.hour.grid(column=1, row=4, columnspan=2)

        #Ridership Button
        self.getRidership = Button(self, text='Predict!', fg='green', command=self.get_ridership)
        self.getRidership.grid(column=1, row=5)

        #Prediction Message
        self.ridership = Message(self, text='Enter a date and press the "Predict!" button!\nFor May 7th, 2015 at 2pm input 2015, 5, 7, 14', width=200)
        self.ridership.grid(column=1, row=6, columnspan=1)

        #Create a graph space holder
        f = Figure(figsize=(4,4), dpi=100)
        a = f.add_subplot(111)
        a.plot()
        a.set_title('Input a Time to See Trends!')
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().grid(column=3, row=0, rowspan=8)

        #Quit Button
        self.QUIT = Button(self, text='Quit', fg='red', width = 20, command=self.quit)
        self.QUIT.grid(column=1, row=7, columnspan=2)


if __name__ == '__main__':
    print 'Hubway data: loading...'
    hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))
    print 'Hubway data: complete'
    print 'Prediction model: loading...'
    ridershipModelImminent = pickle.load(open('LargeDataStorage/mlModel', 'rb'))
    ridershipModelFar = pickle.load(open('LargeDataStorage/mlModelNoWeather', 'rb'))
    print 'Prediction model: complete'
    UI = UserInterface()
    UI.mainloop()