from django.db import models
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    if not value.name.endswith('.mp4'):
        raise ValidationError(u'Для загрузки разрешены только файлы формата mp4')


# Create your models here.
class Upload(models.Model):
    upload_file = models.FileField(validators=[validate_file_extension])    
    upload_date = models.DateTimeField(auto_now_add=True)
    status: str = "no status"
    result: str = ""
