from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList
from wtforms.form import Form
from wtforms.validators import DataRequired, Length, Regexp

reg_name = Regexp("^[a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ ]*$", message="Name can only contain letters.")
reg_group = Regexp("^[a-zA-Z0-9ąćęłńóśźżĄĘŁŃÓŚŹŻ _-]*$", message="Group name/key can only contain letters, numbers or '_' and '-'.")

class NameEntryForm(Form):
    name = StringField(validators=[Length(1, 32), reg_name])

class GroupForm(FlaskForm):
    group_name  = StringField("Group name", validators=[DataRequired(), Length(1, 32), reg_group])
    names       = FieldList( FormField(NameEntryForm), label="List of names", min_entries=1 )
    submit      = SubmitField("Create")
