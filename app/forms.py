from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    """form that collects query input from the user"""
    queryString = StringField('movie', validators=[DataRequired()])
    submit = SubmitField('Search')

class ResultForm(FlaskForm):
    title = StringField()
    imdbID = StringField()
    year = StringField()

class MultiResultForm(FlaskForm):
    results = FieldList(FormField(ResultForm))
