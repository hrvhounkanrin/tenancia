from django.db import models
from .baseModel import BaseModel
from countries_plus.models import Country

class Banque(BaseModel):
    codebanque=models.CharField(max_length=25, unique=True)
    libbanque=models.CharField(max_length=100)
    pays = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)