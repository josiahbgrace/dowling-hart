import os
from utility import return_file_years
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/background/')
def background():
    name_year = return_file_years("./text/background")
    return render_template('background.html', items=name_year)

def calculate_timeline_placement(buffer):
    """
    Calculate the individual placement of each of the timeline circles using
    the input name_year information. 
    """



if __name__ == '__main__':
    app.run(debug=True)
