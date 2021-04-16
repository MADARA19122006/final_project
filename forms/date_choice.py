from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired


class DateForm(FlaskForm):
    check_in = DateField('Дата заезда', validators=[DataRequired()])
    check_out = DateField('Дата выезда', validators=[DataRequired()])
    submit = SubmitField('Найти номера')
