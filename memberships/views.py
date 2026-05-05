from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .services import MembershipService
from .models import MembershipPlan, Membership
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone



class ActivateMembershipView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get("email")
        plan_name = request.data.get("plan_name")

        MembershipService.activate_membership(email, plan_name)

        return Response({"message": "Membership activated"})
    

class MembershipPlanListView(APIView):
    def get(self, request):
        plans = MembershipPlan.objects.all()
        data = [
            {"id": plan.id, "name": plan.name}
            for plan in plans
        ]
        return Response(data)
    
class MyMembershipView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        membership = Membership.objects.filter(user=user).order_by("-end_date").first()

        if not membership:
            return Response({
                "active": False,
                "plan": None,
                "end_date": None,
                "days_left": None
            })

        today = timezone.now()

        # SAFE access
        plan_name = membership.plan.name if membership.plan else None
        end_date = membership.end_date

        # SAFE validity
        try:
            is_active = membership.is_valid()
        except:
            is_active = False

        # SAFE days calc
        if end_date:
            days_left = (end_date - today).days
            days_left = max(days_left, 0)
        else:
            days_left = None

        return Response({
            "active": is_active,
            "plan": plan_name,
            "end_date": end_date,
            "days_left": days_left
        })