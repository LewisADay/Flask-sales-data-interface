# Flask sales data interface

A simple Flask wrapper for sales data stored as csv's.
Please note this is my first Flask project, and I had plenty of arguments with Pandas along the way, mainly about data types.
This is likely, therefore, not the best implementation, but it was reasonably quick to write in the end, once I'd settled on Pandas.

## Running

To run the program, proceed as follows:

First clone the repo.

> git clone https://github.com/LewisADay/Flask-sales-data-interface.git

Then follow the install instructions for Flask found here: https://flask.palletsprojects.com/en/1.1.x/installation/.

Creating the virtual enviroment in the repo folder.

Then install pandas with pip.

> pip install Pandas

You may then export and run the server program.

> export FLASK_APP=server

> flask run

This starts the server which may then be visited in your broswer at: http://127.0.0.1:5000.

To retrieve the data for a given date, please enter the date in the provided text box and submit, you should then be greeted with a page summerising the data.

You may also retrieve an arbitrary dates data by navigating to http://127.0.0.1:5000/<date>, where <date> is the required date in YYYY-MM-DD format.
