from Tkinter import *
from hubway_collection import *
from weather_collection import *

hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))
# ridershipModel = pickle.load(open('LargeDataStorage/File', 'rb'))

class UserInterface(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createUI()


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
        displays the predicted ridership data for that hour.
        """

        #Gather the requested date
        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())
        hour = int(self.hour.get())
        date = '%i/%i/%i @%i' %(month, day, year, hour)

        if year in hubway.data.keys() and month in hubway.data[year].keys() and day in hubway.data[year][month].keys() and hour in hubway.data[year][month][day].keys():
            numRides = hubway.total_rides_in_hour(year, month, day, hour)
        else:
            forecast = get_imminent_temp_precip_snow(year, month, day, hour)
            forecastedTemp = forecast[0]
            forcastedPrecip = forecast[1]
            forcastedSnow = forecast[2]
            numRides = ridershipModel.predict(np.array([year, month, day, hour, forecastedTemp, forcastedPrecip, forcastedSnow]))

        self.ridership['text'] = '%i rides on %s' %(numRides, date)


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

        #Temperature Button
        self.getTemp = Button(self, text='Get Temp!', fg='green', command=self.get_temp)
        self.getTemp.grid(column=2, row=4)

        #Prediction Message
        self.ridership = Message(self, text='Enter a date and press the "Predict!" button!', width=200)
        self.ridership.grid(column=1, row=5, columnspan=1)

        #Temperature Message
        self.temp = Message(self, text='Enter a date and press the "Get Temp!" button!', width=200)
        self.temp.grid(column=2, row=5, columnspan=1)

        #Quit Button
        self.QUIT = Button(self, text='Quit', fg='red', width = 20, command=self.quit)
        self.QUIT.grid(column=1, row=6, columnspan=2)


UI = UserInterface()
UI.mainloop()