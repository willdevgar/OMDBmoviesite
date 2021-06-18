from flask import render_template, request, flash, redirect, url_for
from app import app, models
from app.forms import SearchForm, MultiResultForm, ResultForm
from app import db
from app.models import result
import requests
import json
import urllib.request as pull 

@app.route('/')
@app.route('/index') 
def index():
    form = SearchForm()
    return render_template('index.html', title='Home', form=form)

@app.route('/search', methods=["POST"])
def search():
    form = ResultForm()
     
    # clearing the database of existing data to avoid duplicates
    db.session.query(result).delete()
    db.session.commit()
    
    # receives the incoming POST request from the form and turns it into text
    text =request.form['text']
    # processes the text into a string format to add to the API query string
    text_two = text.split()
    processed = "+".join(text_two)
    to_be_returned_from_OMDB ="https://www.omdbapi.com/?s="+processed+"&page=1&apikey=e3c04726"
    # uses the 'urllib.request as pull' to open the url as a response and then open as a dictionary with data
    with pull.urlopen(to_be_returned_from_OMDB) as response:
        source = response.read()
        data = json.loads(source)
    search_list =  data["Search"]
    for movie in search_list:
        result1 = result(imdbID=movie["imdbID"], title=movie["Title"], year=movie["Year"])
        db.session.add(result1)
        db.session.commit()
    return render_template('search.html', title="Results", results=search_list, form=form)

@app.route('/details', methods=["POST"])
def details():
    text_id = request.form['imdbID']
    to_be_returned_from_OMDB ="https://www.omdbapi.com/?i="+text_id+"&apikey=e3c04726"

def _add_to_db(text):
    """function for addiing json object results to db depending on result amount and returning a SQLAlchemy object"""
    # starts of by getting the url for the first page of results 
    url_string = _string_to_url(text, 1)
    # stores the JSON object from the api as a python dictionary
    with pull.urlopen(url_string) as response:
        source = response.read()
        data = json.loads(source)
    
    if data["Response"] == "False":
        # if the json object found no results, then redirect back to the home search screen
        flash("No results, please enter new search terms")
        return redirect("/index")
    # otherwise, if response is at least one ...
    else:
        search_list = None
        if data["totalResults"] <= 10:
            for movie in search_list:
                result1 = result(imdbID=movie["imdbID"], title=movie["Title"], year=movie["Year"])
                db.session.add(result1)
                db.session.commit()
            search_list = db.session.query(result).all()
        # otherwise, data["totalResults"] > 10
        else:
            for i in range(1,6):
                if data["totalResults"] < 20:
                    # change_url by passing to _string_to_url for text, num = 2)
                    # add to db
                elif data["totalResults"] < 30:
                    # change_url by passing to _string_to_url for text, num = 2)
                    # add to db
                # ....and so on until we return the JSON object, DO WE NEED TO RETURN A JSON OBJECT?


def _string_to_url(text, num):
    """function for converting text to a url for omdb api
    param: text string
    param: specific page number of total results to return"""
    text_two = text.split()
    processed = "+".join(text_two)
    to_be_returned_from_OMDB ="https://www.omdbapi.com/?s="+processed+"&page="+num+"&apikey=e3c04726"
    return to_be_returned_from_OMDB
