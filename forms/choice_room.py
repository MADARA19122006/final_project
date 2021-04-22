from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FieldList, HiddenField, StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    rooms = FieldList(SelectField('Qty', choices=[], validate_choice=False))
    ids = FieldList(HiddenField(validators=[DataRequired()]))
    price = FieldList(HiddenField(validators=[DataRequired()]))
    submit = SubmitField('Submit')
