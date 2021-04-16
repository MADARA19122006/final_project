from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FieldList


class RoomForm(FlaskForm):
    rooms = FieldList(SelectField('Qty', choices=[], validate_choice=False))
    submit = SubmitField('Submit')
