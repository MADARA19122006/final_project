from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('имя', validators=[DataRequired()])
    surname = StringField('фамилия', validators=[DataRequired()])
    phone = IntegerField('телефон', validators=[DataRequired()])
    email = EmailField('адрес электронной почты')
    password = StringField('придумайте пароль', validators=[DataRequired()])
    password_again = StringField('повторите пароль', validators=[DataRequired()])
    submit = SubmitField('зарегистрироваться')
