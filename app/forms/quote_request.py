import re
from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    DecimalField,
    EmailField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    NumberRange,
    Optional,
    ValidationError,
)

from ..models.quote_request import EventType


def _clean_contact(value: str | None) -> str | None:
    if not value:
        return None
    return re.sub(r"\s+", " ", value).strip()


class QuoteRequestForm(FlaskForm):
    event_type = SelectField(
        "Type d’événement",
        choices=[(item.value, item.value) for item in EventType],
        validators=[InputRequired()],
    )
    event_date = DateField("Date", validators=[InputRequired()])
    event_time = TimeField("Heure", validators=[Optional()])
    location = StringField(
        "Lieu", validators=[InputRequired(), Length(min=2, max=255)]
    )
    guest_count = IntegerField(
        "Nombre de personnes",
        validators=[InputRequired(), NumberRange(min=1, max=100000)],
    )

    budget_min = DecimalField(
        "Budget minimum", places=2, validators=[Optional(), NumberRange(min=0)]
    )
    budget_max = DecimalField(
        "Budget maximum", places=2, validators=[Optional(), NumberRange(min=0)]
    )
    notes = TextAreaField(
        "Informations complémentaires", validators=[Optional(), Length(max=3000)]
    )

    customer_name = StringField(
        "Nom", validators=[InputRequired(), Length(min=2, max=160)]
    )
    phone = StringField("Téléphone", validators=[Optional(), Length(max=40)])
    whatsapp = StringField("WhatsApp", validators=[Optional(), Length(max=40)])
    email = EmailField(
        "Email", validators=[Optional(), Length(max=254)]
    )

    submission_token = HiddenField(validators=[InputRequired()])
    website = StringField("Site web", validators=[Optional(), Length(max=200)])

    def validate_event_date(self, field):
        if field.data and field.data < date.today():
            raise ValidationError("La date de l’événement ne peut pas être passée.")

    def validate_budget_max(self, field):
        if (
            self.budget_min.data is not None
            and field.data is not None
            and field.data < self.budget_min.data
        ):
            raise ValidationError(
                "Le budget maximum doit être supérieur ou égal au minimum."
            )

    def validate_email(self, field):
        value = _clean_contact(field.data)
        if value and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValidationError("Adresse email invalide.")
        if not any(
            _clean_contact(value)
            for value in (self.phone.data, self.whatsapp.data, field.data)
        ):
            raise ValidationError(
                "Indiquez au moins un téléphone, WhatsApp ou email."
            )

    def validate_website(self, field):
        if field.data:
            raise ValidationError("Envoi refusé.")

    def normalized_phone(self):
        return _clean_contact(self.phone.data)

    def normalized_whatsapp(self):
        return _clean_contact(self.whatsapp.data)

    def normalized_email(self):
        value = _clean_contact(self.email.data)
        return value.lower() if value else None
