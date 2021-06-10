from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    """form that collects query input from the user"""
    queryString = StringField('movie', validators=[DataRequired()])
    submit = SubmitField('Search')

