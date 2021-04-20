from flask_wtf import FlaskForm
from wtforms import SubmitField


class ReviewForm(FlaskForm):
    forward = SubmitField('>>')
    back = SubmitField('<<')

