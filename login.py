from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class LoginForm(FlaskForm):
    company = StringField('Stocks Analysis Engine')
    search = SubmitField('Search')
