from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .serializers import RequestSerializer, ResponseSerializer
from .tasks import find_user_by_phone
from celery.result import AsyncResult


class ViewUserData(APIView):
    @extend_schema(
        responses={202: ResponseSerializer},
        parameters=[
            OpenApiParameter(
                name="phone_number",
                description="Phone number of the user",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="analyzer_id", description="Analyzer ID", required=False, type=str
            ),
            OpenApiParameter(
                name="user_agent",
                description="User Agent",
                required=False,
                type=str,
                enum=["Desktop", "Mobile"],
            ),
            OpenApiParameter(
                name="source_ip", description="Source IP", required=False, type=str
            ),
            OpenApiParameter(
                name="request_id", description="RequestId", required=False, type=str
            ),
        ],
        description="Get user data",
    )
    def get(self, request):
        phone_number = request.GET.get("phone_number")

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=400)

        task = find_user_by_phone.delay(phone_number)
        return Response({"task_id": task.id}, status=202)


class GetTaskResult(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="task_id", description="celery task id", required=True, type=str
            )
        ]
    )
    def get(self, request, task_id):
        result = AsyncResult(id=task_id)

        if result.state == "PENDING":
            return Response({"status": "Pending"}, status=202)
        elif result.state == "SUCCESS":
            return Response(result.result, status=200)
        elif result.state == "STARTED":
            return Response({"status": "Started"}, status=202)
        else:
            return Response(
                {"status": result.state, "message": str(result.info)}, status=400
            )
