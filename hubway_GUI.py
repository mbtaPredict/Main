from Tkinter import *

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

        date = '%s/%s/%s' %(self.month.get(), self.day.get(), self.year.get())
        self.results['text'] = '%i rides on %s' %(5286, date)

    def createUI(self):
        """
        Creates and organizes all the elements of the user interface.
        """

        self.yearLabel = Label(self, text='Year')
        self.yearLabel.grid(column=0, row=0)

        self.year = Entry(self)
        self.year.grid(column=1, row=0)

        self.monthLabel = Label(self, text='Month')
        self.monthLabel.grid(column=0, row=1)

        self.month = Entry(self)
        self.month.grid(column=1, row=1)

        self.dayLabel = Label(self, text='Day')
        self.dayLabel.grid(column=0, row=2)

        self.day = Entry(self)
        self.day.grid(column=1, row=2)

        self.submit = Button(self, text='Predict!', fg='green', command=self.callback)
        self.submit.grid(column=1, row=3)

        self.results = Message(self, text='Results of the prediction go here.', width=200)
        self.results.grid(column=0, row=4, columnspan=2)

        self.QUIT = Button(self, text='Quit', fg='red', command=self.quit)
        self.QUIT.grid(column=1, row=5)

UI = UserInterface()
UI.mainloop()