from pathlib import Path
from uuid import uuid4

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ALLOWED_CATALOG_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
ALLOWED_CATALOG_IMAGE_MIMES = {"image/jpeg", "image/png", "image/webp"}


def save_catalog_image(file: FileStorage | None) -> str | None:
    if not file or not file.filename:
        return None

    safe_name = secure_filename(file.filename)
    if "." not in safe_name:
        raise ValueError("Le fichier image doit avoir une extension.")

    extension = safe_name.rsplit(".", 1)[1].lower()
    if extension not in ALLOWED_CATALOG_IMAGE_EXTENSIONS:
        raise ValueError("Format d’image non autorisé.")

    if file.mimetype and file.mimetype.lower() not in ALLOWED_CATALOG_IMAGE_MIMES:
        raise ValueError("Type MIME d’image non autorisé.")

    upload_root = Path(current_app.config["UPLOAD_FOLDER"])
    catalog_dir = upload_root / "catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)

    generated_name = f"{uuid4().hex}.{extension}"
    file.save(catalog_dir / generated_name)
    return f"uploads/catalog/{generated_name}"
