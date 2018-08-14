from django.db import models
from model_utils import Choices
from .baseModel import BaseModel

class Banque(BaseModel):
    codebanque=models.CharField(max_length=25, unique=True)
    libbanque=models.CharField(max_length=100)