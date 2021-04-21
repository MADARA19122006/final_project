from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField


class EditForm(FlaskForm):
    quantity = IntegerField('Количество номеров')
    price = IntegerField('Цена')
    submit = SubmitField('Редактировать')
