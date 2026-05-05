from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Attendance

from .services import AttendanceService, DayPassService


class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        AttendanceService.check_in(user)

        return Response(
            {"message": "Check-in successful"},
            status=status.HTTP_201_CREATED
        )
    
class DayPassCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        name = request.data.get("name")
        price = request.data.get("price")

        if not name or not price:
            return Response(
                {"detail": "Name and price are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        day_pass = DayPassService.create_day_pass(name=name, price=price)

        return Response(
            {"message": "Day pass created and user checked in"},
            status=status.HTTP_201_CREATED
        )
    
class TodayAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        attendance = Attendance.objects.filter(user=user, date=today).first()

        if attendance:
            return Response({
                "checked_in": True,
                "time": attendance.check_in_time
            })

        return Response({
            "checked_in": False
        })