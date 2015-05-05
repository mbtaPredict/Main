# hubwayPredict

A comprehensive prediction of ridership for Hubway, a bikesharing service in Boston, based on historical ridership and weather conditions.

##Creators
**Kevin Crispie**
- <https://github.com/kevincrispie>

**Shane Kelly**
- <https://github.com/shanek21>

**William Lu**

- <https://github.com/williamalu>


##How To Run:

**Installing Packages**

The Python packages needed to run this code are scikit-learn and numpy. In order to run our ipython notebook, which develops the prediction model, matplotlib and ipython need to be installled.
These packages need to be downloaded in order for the code to run properly. Download instructions for each package are as follows:
 

*scikit-learn*: if you are in Ubuntu, type the following command into terminal:
```
pip install --user --install-option="--prefix=" -U scikit-learn
```
If you are not in Ubuntu, or have problems with the download, futher download instructions can be found on [scikit-learn's website] (http://scikit-learn.org/stable/install.html).

If you already have scikit-learn installed, make sure that it is version 0.15 or higher. This is the earliest version that is able to run the file we have.

*numpy*: if you are in Ubuntu, type the following command into terminal:
```
sudo apt-get install python-numpy
```
If you are not in Ubuntu, or have problems with the download, please see the [installation page](http://www.scipy.org/install.html) on scipy.org

*matplotlib*: if you are in Ubuntu, type the following command into terminal:
```
sudo apt-get install python-matplotlib 
```
If you are not in Ununtu, or have problems with the download, further download instructions can be found on [matplotlib.org](http://matplotlib.org/users/installing.html)

*ipython*: if you are in Ubuntu, type the following command into terminal:
```
pip install "ipython[all]"
```
If you are not in Ubuntu, or have problems with the download, please see the [ipython website](http://ipython.org/install.html)

**Running the GUI**

To use the GUI, type to following command into terminal:
```
python hubway_gui.py
```
This will start running the file. First, the Hubway data will load. This will take around a minute. Next, input the date and time that you would like data for. You can input any date or time. The histrocial data that we have is for Hubway rides during 2011, 2012, and 2013. If the input is a date and time for which we have historical data, the gui displays the historical data. To get a prediction, input a date and time that is less than 240 hours, or 10 days, in the future.  The month should be a number, and the hour should be an integer from 0-23.

The GUI will return the number of rides it predicts during that hour. It can also return the temperature prediction for that hour. Press the Quit button to quit the GUI when you are finished.

**Importing Weather Data**

We have left our own Weather Underground API key in our code. If you plan on obtaining a large amount fo data via the Weather Underground API, please obtain and use your own key. You can do this by going to the [Weather Underground website](http://www.wunderground.com/weather/api/). Sign up by clicking on the orange button that says "Sign Up for FREE!", fill in your information, and you will be given an API key.

**Running the ipython notebook**

To run our ipython notebook, type the following command into terminal:
``` 
ipython notebook lin_reg.ipynb
```
When a webpage opens up, click on the file name that says "lin_reg.ipynb". The ipython notebook will open. Run the python notebook by selecting each section in order and clicking the run arrow at the top of the page. This ipython notebook develops the model we use to predict hubway ridership.
