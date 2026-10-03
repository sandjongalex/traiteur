from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField
from wtforms.validators import InputRequired, Length, Optional


class UserRolesForm(FlaskForm):
    role_ids = SelectMultipleField("Rôles", coerce=int)


class RolePermissionsForm(FlaskForm):
    name = StringField("Nom", validators=[InputRequired(), Length(min=2, max=100)])
    description = StringField("Description", validators=[Optional(), Length(max=255)])
    permission_ids = SelectMultipleField("Permissions", coerce=int)
