from decimal import Decimal

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, DecimalField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, NumberRange, Optional

from ..models.equipment import EquipmentCondition, EquipmentMovementType


IMAGE_EXTENSIONS = ["jpg", "jpeg", "jfif", "png", "webp"]


CONDITION_CHOICES = [
    (EquipmentCondition.NEW.value, "Neuf"),
    (EquipmentCondition.GOOD.value, "Bon"),
    (EquipmentCondition.FAIR.value, "Moyen"),
    (EquipmentCondition.DAMAGED.value, "Endommagé"),
]

MOVEMENT_CHOICES = [
    (EquipmentMovementType.ENTRY.value, "Entrée / achat"),
    (EquipmentMovementType.OUT.value, "Sortie"),
    (EquipmentMovementType.RETURN.value, "Retour"),
    (EquipmentMovementType.MAINTENANCE_OUT.value, "Mise en maintenance"),
    (EquipmentMovementType.MAINTENANCE_RETURN.value, "Retour de maintenance"),
    (EquipmentMovementType.LOSS_AVAILABLE.value, "Perte depuis disponible"),
    (EquipmentMovementType.LOSS_EVENT.value, "Perte pendant une sortie"),
    (EquipmentMovementType.LOSS_MAINTENANCE.value, "Perte en maintenance"),
    (EquipmentMovementType.BREAKAGE_AVAILABLE.value, "Casse depuis disponible"),
    (EquipmentMovementType.BREAKAGE_EVENT.value, "Casse pendant une sortie"),
    (EquipmentMovementType.BREAKAGE_MAINTENANCE.value, "Casse en maintenance"),
    (EquipmentMovementType.ADJUSTMENT_ADD.value, "Ajustement positif"),
    (EquipmentMovementType.ADJUSTMENT_REMOVE.value, "Ajustement négatif"),
]


class EquipmentCategoryForm(FlaskForm):
    name = StringField("Nom", validators=[InputRequired(), Length(max=120)])
    code = StringField("Code", validators=[InputRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=500)])
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Enregistrer")


class EquipmentForm(FlaskForm):
    category_id = SelectField("Catégorie", coerce=int, validators=[InputRequired()])
    name = StringField("Nom du matériel", validators=[InputRequired(), Length(max=160)])
    reference = StringField("Référence interne", validators=[Optional(), Length(max=80)])
    description = TextAreaField("Description", validators=[Optional()])
    unit = StringField("Unité", default="pièce", validators=[InputRequired(), Length(max=40)])
    initial_quantity = DecimalField(
        "Quantité initiale", places=2, default=Decimal("0.00"),
        validators=[InputRequired(), NumberRange(min=0)]
    )
    purchase_price = DecimalField(
        "Prix d’achat unitaire (FCFA)", places=2, validators=[Optional(), NumberRange(min=0)]
    )
    replacement_value = DecimalField(
        "Valeur de remplacement unitaire (FCFA)", places=2,
        validators=[Optional(), NumberRange(min=0)]
    )
    condition = SelectField("État", choices=CONDITION_CHOICES, validators=[InputRequired()])
    image = FileField(
        "Photo", validators=[Optional(), FileAllowed(IMAGE_EXTENSIONS, "Image jpg/jpeg/jfif/png/webp uniquement.")]
    )
    notes = TextAreaField("Notes", validators=[Optional()])
    is_active = BooleanField("Actif", default=True)
    submit = SubmitField("Enregistrer")


class EquipmentMovementForm(FlaskForm):
    movement_type = SelectField("Type de mouvement", choices=MOVEMENT_CHOICES, validators=[InputRequired()])
    quantity = DecimalField(
        "Quantité", places=2, validators=[InputRequired(), NumberRange(min=Decimal("0.01"))]
    )
    note = TextAreaField("Motif / note", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Enregistrer le mouvement")
