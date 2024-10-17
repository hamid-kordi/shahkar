from django.urls import path
from .views import ViewUserData

app_name = "user"

urlpatterns = []


urlpatterns = [
    path("my_view/", ViewUserData.as_view(), name="my_view"),
]
