from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .serializers import RequestSerializer, ResponseSerializer
from .tasks import find_user_by_phone
from celery.result import AsyncResult


class ViewUserData(APIView):
    @extend_schema(
        request=RequestSerializer,
        responses={202, ResponseSerializer},
        description="Get user data",
    )
    def get(self, request):
        analyzer_id = request.GET.get("analyzer_id")
        if not phone_number:
            return Response({"error": "Phone number is required."}, status=400)
        phone_number = request.GET.get("phone_number")
        task = find_user_by_phone.delay(phone_number)
        return Response({"task_id": task.id}, status=202)


class GetTaskResult(APIView):
    def get(self, reqest, task_id):
        result = AsyncResult(id=task_id)
        if result.state == "PENDING":
            return Response({"status": "Pending"}, status=202)
        if result.state == "SUCCESS":
            return Response(result.result, status=200)
        if result.state == "STARTED":
            return Response({"status": "Started"}, status=202)
        else:
            return Response(
                {"status": result.state, "message": str(result.info)}, status=400
            )
