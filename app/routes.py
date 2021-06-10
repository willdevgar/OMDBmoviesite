from flask import render_template, url_for, request
from app import app
from app.forms import SearchForm

@app.route('/')
@app.route('/index') 
def index():
    user = {'username':'Will'}
    form = SearchForm()
    return render_template('index.html', title='Home', form=form)

@app.route('/search', methods=["POST"])
def search_result():
    text =request.form['text']
    text_two = text.split()
    processed = "+".join(text_two)
    to_be_returned_from_OMDB ="https://www.omdbapi.com/?s="+processed+"&apikey=e3c04726"
    return to_be_returned_from_OMDB
