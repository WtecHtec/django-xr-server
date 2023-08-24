import uuid
from django.db import models

# Create your models here.
class XrMaterials(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  app_id = models.CharField(max_length=160)
  target_photo = models.ImageField(upload_to='photos/')
  model_url = models.CharField(max_length=255)
  create_time = models.DateTimeField(auto_now_add=True)
  update_time = models.DateTimeField(auto_now=True)
  

