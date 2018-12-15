from django.db import models
from model_utils import Choices

class BaseModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=100)
    owner = models.CharField(max_length=100,null=True)

    class Meta:
        abstract=True
