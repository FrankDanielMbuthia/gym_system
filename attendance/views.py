from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .services import AttendanceService


class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        AttendanceService.check_in(user)

        return Response(
            {"message": "Check-in successful"},
            status=status.HTTP_201_CREATED
        )