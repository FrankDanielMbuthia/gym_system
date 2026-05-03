from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError

from attendance.models import Attendance
from attendance.services import AttendanceService
from memberships.models import Membership, MembershipPlan


class AttendanceServiceTest(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

        self.user = self.user_model.objects.create_user(
            username="member",
            password="pass123",
            is_active=True
        )

        self.plan = MembershipPlan.objects.create(
            name="Basic",
            price=1000,
            duration=30
        )

        self.membership = Membership.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            is_active=True
        )

    # ✅ Test 1: Successful check-in
    def test_check_in_success(self):
        attendance = AttendanceService.check_in(self.user)
        self.assertIsNotNone(attendance)

    # ❌ Test 2: Cannot check-in twice
    def test_cannot_check_in_twice(self):
        AttendanceService.check_in(self.user)

        with self.assertRaises(ValidationError):
            AttendanceService.check_in(self.user)

    # ❌ Test 3: Cannot check-in without membership
    def test_cannot_check_in_without_membership(self):
        self.membership.delete()

        with self.assertRaises(ValidationError):
            AttendanceService.check_in(self.user)

    # ❌ Test 4: Cannot check-in if membership expired
    def test_cannot_check_in_if_membership_expired(self):
        self.membership.end_date = timezone.now() - timedelta(days=1)
        self.membership.save()

        with self.assertRaises(ValidationError):
            AttendanceService.check_in(self.user)

    # ❌ Test 5: Cannot check-in if user inactive
    def test_cannot_check_in_if_user_inactive(self):
        self.user.is_active = False
        self.user.save()

        with self.assertRaises(ValidationError):
            AttendanceService.check_in(self.user)