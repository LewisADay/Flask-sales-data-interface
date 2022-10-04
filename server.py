
from flask import Flask, render_template, redirect, request, url_for
from markupsafe import escape
from query import Query, is_valid_date

app = Flask(__name__)

# redirects to index page if coming to "/""
@app.route('/')
def wp_entry():
    return redirect(url_for('index'))

# on the index page link up the form with appropriate HTTP methods
@app.route('/index', methods=['POST', 'GET'])
def index():
    # If we're receiving the forms details
    if request.method == 'POST':
        # Get the date
        input = request.form['date']
        # Escape it to prevent injection attacks (why not, it's good practice)
        input = escape(input)
        # If a valid date
        if is_valid_date(input):
            # Take us to the page for that date's details
            return redirect(input)
        else:
            # Otherwise display error and explain format
            # (handled in the template)
            return render_template('index.html', prev=input)
    else:
        # Render the template by default
        return render_template('index.html')

# For all urls of the form, take the date as an input
# and get it's data
@app.route('/<date>/')
def wp_date(date):
    # Run the query on this date
    # maybe this should be through a .run method or something
    # I don't like my OOP in this I must say
    # I only really used any so we can call attributes in the template
    query = Query(date)
    # Render out the template with the query's data
    return render_template('date.html', query=query)

# My first Flask program - it seems neat, I've decided I need to brush up
# on my HTML and my HTTP requests etc. but I like it, quite simple at the
# end of the day, but did take me a while to grasp to begin with

if __name__ == '__main__':
    app.run(debug = True)
    