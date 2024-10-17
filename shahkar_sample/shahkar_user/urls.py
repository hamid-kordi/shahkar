from django.urls import path
from .views import ViewUserData, GetTaskResult

app_name = "user"

urlpatterns = []


urlpatterns = [
    path("my_view/", ViewUserData.as_view(), name="my_view"),
    path("task_result/", GetTaskResult.as_view(), name="result"),
]
