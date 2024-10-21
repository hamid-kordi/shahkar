from django.db import models
from django.core.exceptions import ValidationError
import uuid

# Create your models here.


class UserProfile(models.Model):
    phonenumber = models.CharField(max_length=13, db_index=True)
    natoinal_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateTimeField()
    address = models.CharField(max_length=255)

    def clean_phonenumber(self):
        if len(self.phonenumber) != 11:
            raise ValidationError(message="phone number must be 11 integer")


class UserAnalyzer(models.Model):
    analyzer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)


