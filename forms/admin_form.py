from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, IntegerField


class AdminForm(FlaskForm):
    check_in_from = DateField('Заезд c')
    check_in_to = DateField('Заезд по')
    check_out_from = DateField('Выезд с')
    check_out_to = DateField('Выезд по')
    number_booking = IntegerField('Номер брони')
    submit = SubmitField('Искать')
