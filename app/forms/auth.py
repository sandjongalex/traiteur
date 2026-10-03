from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField
from wtforms.validators import EqualTo, InputRequired, Length, Optional, ValidationError


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Length(max=254)])
    password = PasswordField("Mot de passe", validators=[InputRequired(), Length(max=255)])
    remember = BooleanField("Se souvenir de moi")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Mot de passe actuel", validators=[InputRequired()])
    new_password = PasswordField("Nouveau mot de passe", validators=[InputRequired(), Length(min=12, max=255)])
    confirm_password = PasswordField(
        "Confirmer le nouveau mot de passe",
        validators=[InputRequired(), EqualTo("new_password", message="Les mots de passe ne correspondent pas.")],
    )


class UserForm(FlaskForm):
    first_name = StringField("Prénom", validators=[InputRequired(), Length(min=2, max=100)])
    last_name = StringField("Nom", validators=[InputRequired(), Length(min=2, max=100)])
    email = EmailField("Email", validators=[InputRequired(), Length(max=254)])
    phone = StringField("Téléphone", validators=[Optional(), Length(max=40)])


class CreateUserForm(UserForm):
    password = PasswordField("Mot de passe initial", validators=[InputRequired(), Length(min=12, max=255)])


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField("Nouveau mot de passe", validators=[InputRequired(), Length(min=12, max=255)])
    confirm_password = PasswordField(
        "Confirmer le mot de passe",
        validators=[InputRequired(), EqualTo("new_password", message="Les mots de passe ne correspondent pas.")],
    )
