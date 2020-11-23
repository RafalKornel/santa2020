from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList, BooleanField
from wtforms.form import Form
from wtforms.validators import DataRequired, Length, Regexp

reg_name = Regexp("^[a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ ]*$", message="Name can only contain letters.")
reg_PIN = Regexp("^[0-9]{4}$", message="PIN is 4 digits.")
reg_group = Regexp("^[a-zA-Z0-9ąćęłńóśźżĄĘŁŃÓŚŹŻ _-]*$", message="Group name/key can only contain letters, numbers or '_' and '-'.")

class NameEntryForm(Form):
    name = StringField(validators=[DataRequired(), Length(1, 32), reg_name])
    pin = StringField(validators=[Length(4), reg_PIN], default="0000")


class GroupForm(FlaskForm):
    group_name  = StringField("Group name", validators=[DataRequired(), Length(1, 32), reg_group])
    secure      = BooleanField("Secure")
    names       = FieldList( FormField(NameEntryForm), label="Names of users", min_entries=1 )
    submit      = SubmitField("Create")
