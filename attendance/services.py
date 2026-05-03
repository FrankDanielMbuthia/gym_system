from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from .models import Attendance
from memberships.models import Membership

from .models import DayPass

class DayPassService:

    @staticmethod
    def create_day_pass(user, price):
        today = timezone.now().date()

        if DayPass.objects.filter(user=user, date=today).exists():
            raise ValidationError({"detail": "Day pass already exists for today."})

        return DayPass.objects.create(user=user, price=price)

class AttendanceService:

    @staticmethod
    def check_in(user):

        if not user.is_active:
            raise ValidationError({"detail": "User account is not active."})

        today = timezone.now().date()

        membership = Membership.objects.filter(user=user).order_by("-end_date").first()
        has_valid_membership = membership and membership.is_valid()

        has_day_pass = DayPass.objects.filter(user=user, date=today).exists()

        if not (has_valid_membership or has_day_pass):
            raise ValidationError({"detail": "No valid membership or day pass."})

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