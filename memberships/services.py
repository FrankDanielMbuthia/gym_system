from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError
from .models import Membership, MembershipPlan
from accounts.models import User

class MembershipService:

    @staticmethod
    def activate_membership(user_id, plan_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError({"detail": "User not found."})

        try:
            plan = MembershipPlan.objects.get(id=plan_id)
        except MembershipPlan.DoesNotExist:
            raise ValidationError({"detail": "Plan not found."})

        latest_membership = Membership.objects.filter(user=user).order_by("-end_date").first()

        if latest_membership and latest_membership.is_valid():
            raise ValidationError({
                "detail": "User already has an active membership."
            })

        start_date = timezone.now()
        end_date = start_date + timedelta(days=plan.duration)

        membership = Membership.objects.create(
            user=user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            is_active=True  
        )

        user.is_active = True
        user.save()

        return membership