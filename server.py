
from flask import Flask, render_template, redirect, request, url_for
from markupsafe import escape
from query import Query, is_valid_date

app = Flask(__name__)

@app.route('/')
def wp_entry():
    return redirect(url_for('index'))

@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        input = request.form['date']
        input = escape(input)
        if is_valid_date(input):
            return redirect(input)
        else: # Else return to index with the prev input as param for message
            return render_template('index.html', prev=input)
    else:
        return render_template('index.html')

@app.route('/<date>/')
def wp_date(date):
    query = Query(date)
    return render_template('date.html', query=query)

if __name__ == '__main__':
    app.run(debug = True)