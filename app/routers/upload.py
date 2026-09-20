import os
import uuid

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.dependencies.authorization import require_admin

router = APIRouter(
    prefix="/upload",
    tags=["File Upload"]
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("")
def upload_image(
    file: UploadFile = File(...),
    current_admin=Depends(require_admin)
):
    allowed_types = ["image/jpeg", "image/png"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG and PNG images are allowed"
        )

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    with open(file_path, "wb") as image:
        image.write(file.file.read())

    return {
        "message": "Image uploaded successfully",
        "filename": unique_filename,
        "file_path": file_path
    }