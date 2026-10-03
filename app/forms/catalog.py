from decimal import Decimal

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    DecimalField,
    IntegerField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import InputRequired, Length, NumberRange, Optional, ValidationError

from ..models.catalog import CategoryType, PricingUnit

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]


def _pricing_choices():
    labels = {
        PricingUnit.FIXED.value: "Prix fixe",
        PricingUnit.PER_PERSON.value: "Par personne",
        PricingUnit.PER_UNIT.value: "Par unité",
        PricingUnit.PER_HOUR.value: "Par heure",
        PricingUnit.ON_REQUEST.value: "Sur devis",
    }
    return [(item.value, labels[item.value]) for item in PricingUnit]


class AdminAccessForm(FlaskForm):
    access_key = PasswordField("Clé d’accès", validators=[InputRequired(), Length(max=256)])
    submit = SubmitField("Accéder au catalogue")


class CategoryForm(FlaskForm):
    name = StringField("Nom", validators=[InputRequired(), Length(max=120)])
    slug = StringField("Slug", validators=[Optional(), Length(max=140)])
    description = TextAreaField("Description", validators=[Optional()])
    category_type = SelectField(
        "Type",
        choices=[(item.value, item.value.title()) for item in CategoryType],
        validators=[InputRequired()],
    )
    display_order = IntegerField(
        "Ordre d’affichage", default=0, validators=[InputRequired(), NumberRange(min=0)]
    )
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Enregistrer")


class BaseCatalogItemForm(FlaskForm):
    name = StringField("Nom", validators=[InputRequired(), Length(max=160)])
    slug = StringField("Slug", validators=[Optional(), Length(max=180)])
    short_description = StringField(
        "Description courte", validators=[Optional(), Length(max=320)]
    )
    description = TextAreaField("Description", validators=[Optional()])
    pricing_unit = SelectField(
        "Tarification", choices=_pricing_choices(), validators=[InputRequired()]
    )
    image = FileField(
        "Image",
        validators=[
            Optional(),
            FileAllowed(IMAGE_EXTENSIONS, "Format autorisé : jpg, jpeg, png ou webp."),
        ],
    )
    is_featured = BooleanField("Mettre en avant")
    is_active = BooleanField("Actif", default=True)
    is_public = BooleanField("Publié")
    display_order = IntegerField(
        "Ordre d’affichage", default=0, validators=[InputRequired(), NumberRange(min=0)]
    )
    submit = SubmitField("Enregistrer")

    def validate_price_for_unit(self, field):
        if self.pricing_unit.data != PricingUnit.ON_REQUEST.value and field.data is None:
            raise ValidationError("Un prix est requis pour ce type de tarification.")
        if field.data is not None and Decimal(field.data) < 0:
            raise ValidationError("Le prix doit être positif ou nul.")


class ServiceForm(BaseCatalogItemForm):
    base_price = DecimalField(
        "Prix de base", places=2, validators=[Optional(), NumberRange(min=0)]
    )

    def validate_base_price(self, field):
        self.validate_price_for_unit(field)


class DishForm(BaseCatalogItemForm):
    category_id = SelectField("Catégorie", coerce=int, validators=[Optional()])
    base_price = DecimalField(
        "Prix de base", places=2, validators=[Optional(), NumberRange(min=0)]
    )

    def validate_base_price(self, field):
        self.validate_price_for_unit(field)


class MenuForm(BaseCatalogItemForm):
    price = DecimalField("Prix", places=2, validators=[Optional(), NumberRange(min=0)])
    minimum_people = IntegerField(
        "Minimum de personnes", validators=[Optional(), NumberRange(min=1)]
    )
    dish_ids = SelectMultipleField("Plats du menu", coerce=int, validators=[Optional()])

    def validate_price(self, field):
        self.validate_price_for_unit(field)


class PackForm(BaseCatalogItemForm):
    price = DecimalField("Prix", places=2, validators=[Optional(), NumberRange(min=0)])
    minimum_people = IntegerField(
        "Minimum de personnes", validators=[Optional(), NumberRange(min=1)]
    )
    dish_ids = SelectMultipleField("Plats inclus", coerce=int, validators=[Optional()])
    menu_ids = SelectMultipleField("Menus inclus", coerce=int, validators=[Optional()])
    service_ids = SelectMultipleField(
        "Services inclus", coerce=int, validators=[Optional()]
    )

    def validate_price(self, field):
        self.validate_price_for_unit(field)
