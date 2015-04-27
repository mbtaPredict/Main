from Tkinter import *
from hubway_collection import *

hubway = pickle.load(open('LargeDataStorage/hubwayDataFile', 'rb'))

class UserInterface(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createUI()


    def callback(self):
        """
        When the user presses the Predict button this function is called. This function
        displays the requested results.
        """

        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())

        date = '%i/%i/%i' %(month, day, year)
        self.results['text'] = '%i rides on %s' %(hubway.total_rides_in_day(year, month, day), date)


    def createUI(self):
        """
        Creates and organizes all the elements of the user interface.
        """

        #Window title
        self.master.title('hubwayPredict')

        #Year
        self.yearLabel = Label(self, text='Year')
        self.yearLabel.grid(column=0, row=0)

        self.year = Entry(self)
        self.year.grid(column=1, row=0)

        #Month
        self.monthLabel = Label(self, text='Month')
        self.monthLabel.grid(column=0, row=1)

        self.month = Entry(self)
        self.month.grid(column=1, row=1)

        #Day
        self.dayLabel = Label(self, text='Day')
        self.dayLabel.grid(column=0, row=2)

        self.day = Entry(self)
        self.day.grid(column=1, row=2)

        #Predict
        self.predict = Button(self, text='Predict!', fg='green', command=self.callback)
        self.predict.grid(column=1, row=3)

        #Results
        self.results = Message(self, text='Enter a date and press the "Predict" button!', width=200)
        self.results.grid(column=0, row=4, columnspan=2)

        #Quit
        self.QUIT = Button(self, text='Quit', fg='red', command=self.quit)
        self.QUIT.grid(column=1, row=5)

UI = UserInterface()
UI.mainloop()