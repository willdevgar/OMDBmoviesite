from flask import render_template, request
from app import app
from app.forms import SearchForm, MultiResultForm, ResultForm
from app import db
from app.models import result
import requests
import json
import urllib.request as pull 

@app.route('/')
@app.route('/index') 
def index():
    user = {'username':'Will'}
    form = SearchForm()
    return render_template('index.html', title='Home', form=form)

@app.route('/search', methods=["POST"])
def search():
    
    # receives the incoming POST request from the form and turns it into text
    text =request.form['text']
    # processes the text into a string format to add to the API query string
    text_two = text.split()
    processed = "+".join(text_two)
    to_be_returned_from_OMDB ="https://www.omdbapi.com/?s="+processed+"&apikey=e3c04726"
    # uses the 'urllib.request as pull' to open the url as a response and then open as a dictionary with data
    with pull.urlopen(to_be_returned_from_OMDB) as response:
        source = response.read()
        data = json.loads(source)
    search_list =  data["Search"]
#    result1 = None
#    for movie in search_list:
#        result1 = result(imdbID=movie["imdbID"], title=movie["Title"], year=movie["Year"])
#        db.session.add(result1)
#    db.session.commit()
#    dummy_result = result(imdbID="n00", title="Nada",year="1800")
#    results = result1.query.all()
    return render_template('search.html', title="Results", results=search_list)
