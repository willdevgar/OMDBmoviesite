from flask import render_template, url_for
from app import app
from app.forms import SearchForm

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    user = {'username':'Will'}
    form = SearchForm()
    return render_template('index.html', title='Home', form=form)


