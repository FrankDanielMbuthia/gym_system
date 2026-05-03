from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError

from memberships.models import MembershipPlan, Membership
from memberships.services import MembershipService


class MembershipServiceTest(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username="testuser",
            password="pass123",
            is_active=False
        )

        self.plan = MembershipPlan.objects.create(
            name="Basic",
            price=1000,
            duration=30
        )

    
    def test_activate_membership_success(self):
        membership = MembershipService.activate_membership(
            user_id=self.user.id,
            plan_id=self.plan.id
        )

        self.assertIsNotNone(membership)
        self.assertTrue(self.user_model.objects.get(id=self.user.id).is_active)
        self.assertEqual(membership.user, self.user)

    
    def test_cannot_activate_if_valid_membership_exists(self):
        MembershipService.activate_membership(self.user.id, self.plan.id)

        with self.assertRaises(ValidationError):
            MembershipService.activate_membership(self.user.id, self.plan.id)

    
    def test_can_activate_after_expiry(self):
        membership = MembershipService.activate_membership(self.user.id, self.plan.id)

        # Expire the membership manually
        membership.end_date = timezone.now() - timedelta(days=1)
        membership.save()

        new_membership = MembershipService.activate_membership(self.user.id, self.plan.id)

        self.assertIsNotNone(new_membership)