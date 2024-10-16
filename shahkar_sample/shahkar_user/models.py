from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class User(models.Model):
    phonenumber = models.CharField(max_length=11)
    nathinal_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateTimeField()
    address = models.CharField(max_length=255)

    def clean_phonenumber(self):
        if len(self.phonenumber) != 11:
            raise ValidationError(message="phone number must be 11 integer")


class Analyzer(models.Model):
    name = models.CharField(max_length=50)
    
