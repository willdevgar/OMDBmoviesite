from flask import render_template, request, flash, redirect, url_for
from app import app, models
from app.forms import SearchForm, ResultForm
from app import db
from app.models import result
import requests
import json
import urllib.request as pull 

@app.route('/')
@app.route('/index') 
def index():
    form = SearchForm()
    # clearing the database of existing data to avoid duplicates
    db.session.query(result).delete()
    db.session.commit()
    return render_template('index.html', title='Home', form=form)

@app.route('/search', methods=["GET","POST"], defaults={"page":1})
@app.route("/search/<int:page>", methods=["GET"])
def search(page):
    form = ResultForm()
    if request.method =='POST':
        # receives the incoming POST request from the form and turns it into text
        text = request.form['text'] 
        # processes the text into a string format to add to the API query string
        results = _return_json(text) 
        if results is False:
            flash("No results found, please enter new search terms")
            return redirect("/index")
        search_results = results.paginate(page, app.config["RESULTS_PER_PAGE"], False)
        next_url = url_for('search', page=search_results.next_num) if search_results.has_next else None
        prev_url = url_for('search', page=search_results.prev_num) if search_results.has_prev else None
        return render_template('search.html', title="Results", results=search_results.items, form=form, next_url=next_url, prev_url=prev_url)
    else:
        results = db.session.query(result).paginate(page, app.config["RESULTS_PER_PAGE"], False)
        next_url = url_for('search', page=results.next_num) if results.has_next else None
        prev_url = url_for('search', page=results.prev_num) if results.has_prev else None
        return render_template('search.html', title="Results", results=results.items, form=form, next_url=next_url, prev_url=prev_url)

@app.route('/details', methods=["POST"])
def details():
    text_id = request.form['imdbID']
    to_be_returned_from_OMDB ="https://www.omdbapi.com/?i="+text_id+"&apikey=e3c04726"
    with pull.urlopen(to_be_returned_from_OMDB) as response:
        source = response.read()
        data = json.loads(source)
    move_title = data["Title"]
    year = data["Year"]
    released = data["Released"]
    runtime = data["Runtime"]
    genre = data["Genre"]
    director = data["Director"]
    return render_template('movie_detail.html', movie_title=movie_title, year=year, released=released, runtime=runtime, genre=genre,director=director)

def _return_json(text):
    """function for addiing json object results to db depending on result amount and returning a SQLAlchemy object"""
    # starts of by getting the url for the first page of results 
    url_string = _string_to_url(text, 1)
    # stores the JSON object from the api as a python dictionary
    with pull.urlopen(url_string) as response:
        source = response.read()
        data = json.loads(source)
    
    if data["Response"] == "False":
        # if the json object found no results, then redirect back to the home search screen
        return False 
    # otherwise, if response is at least one ...
    else:
        total_results = int(data["totalResults"])
        total_pages = total_results // 10
        if total_pages >= 5:
            for i in range(1,6):
                url_string = _string_to_url(text,i)
                _add_to_db(url_string)
            return db.session.query(result)
        else:
            for i in range(1,total_pages + 1):
                url_string = _string_to_url(text,i)
                _add_to_db(url_string)
            return db.session.query(result)

def _string_to_url(text, num):
    """function for converting text to a url for omdb api
    param: text string
    param: specific page number of total results to return"""
    text_two = text.split()
    processed = "+".join(text_two)
    to_be_returned_from_OMDB ="https://www.omdbapi.com/?s="+processed+"&page="+str(num)+"&apikey=e3c04726"
    return to_be_returned_from_OMDB

def _add_to_db(url_string):
    """ helper function for _return_json function that adds json object results to database (db)"""

    # uses the 'urllib.request as pull' to open the url as a response and then open as a dictionary with data
    with pull.urlopen(url_string) as response:
        source = response.read()
        data = json.loads(source)
    search_list = data["Search"]
    for movie in search_list:
        result1 = result(imdbID=movie["imdbID"], title=movie["Title"], year=movie["Year"])
        db.session.add(result1)
        db.session.commit()
