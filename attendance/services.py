from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from .models import Attendance, DayPass
from memberships.models import Membership


class DayPassService:

    @staticmethod
    def create_day_pass(name, price):
        today = timezone.now().date()

        if DayPass.objects.filter(name=name, date=today).exists():
            raise ValidationError({"detail": "Day pass already exists for today."})

        day_pass = DayPass.objects.create(name=name, price=price)

        Attendance.objects.create(day_pass=day_pass)

        return day_pass


class AttendanceService:

    @staticmethod
    def check_in(user):

        if not user.is_active:
            raise ValidationError({"detail": "User account is not active."})

        today = timezone.now().date()

        membership = Membership.objects.filter(user=user).order_by("-end_date").first()

        if not membership or not membership.is_valid():
            raise ValidationError({"detail": "No valid membership found."})

        already_checked_in = Attendance.objects.filter(
            user=user,
            date=today
        ).exists()

        if already_checked_in:
            raise ValidationError({"detail": "User has already checked in today."})

        try:
            attendance = Attendance.objects.create(user=user)
        except IntegrityError:
            raise ValidationError({"detail": "User has already checked in today."})

        return attendance