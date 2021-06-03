from flask import render_template
from app import app
from app.forms import SearchForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Will'}
    form = SearchForm()
    return render_template('index.html', title='Home', form=form)


