from django.contrib import admin
from .models import User, Analyzer

# Register your models here.


@admin.site(User)
class AdminUser(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "phonenumber",
        "natoinal_id",
        "birthday",
        "address",
    ]


@admin.site(Analyzer)
class AdminAnalyzer(admin.ModelAdmin):
    list_display = ["id", "name"]
