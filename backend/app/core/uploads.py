from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.exceptions import BusinessError

ALLOWED_IMAGE_TYPES = {
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/webp': '.webp',
}


def save_avatar_file(file: UploadFile, target_dir: str, max_bytes: int) -> str:
    suffix = ALLOWED_IMAGE_TYPES.get(file.content_type or '')
    if not suffix:
        raise BusinessError('仅支持 JPG、PNG、WEBP 图片', status_code=400)
    content = file.file.read()
    if len(content) > max_bytes:
        raise BusinessError('头像图片不能超过 2MB', status_code=400)
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    filename = f'{uuid4().hex}{suffix}'
    target_path = Path(target_dir) / filename
    target_path.write_bytes(content)
    return filename
