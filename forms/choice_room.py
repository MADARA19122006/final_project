from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FieldList, HiddenField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    rooms = FieldList(SelectField('Qty', choices=[], validate_choice=False))
    ids = FieldList(HiddenField(validators=[DataRequired()]))
    price = FieldList(HiddenField(validators=[DataRequired()]))
    checkin = HiddenField(validators=[DataRequired()])
    checkout = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Submit')
