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


class ApiLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(max_length=255)
    analyzer_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    phonenumber = models.CharField(max_length=13, db_index=True)
    response_time = models.FloatField(null=True, blank=True)
    result_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    request_size = models.IntegerField()

    class Meta:
        verbose_name = "API Log"
        verbose_name_plural = "API Logs"
