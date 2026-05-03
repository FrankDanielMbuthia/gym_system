from django.utils import timezone
from attendance.models import Attendance
from memberships.models import Membership
from attendance.models import DayPass
from django.contrib.auth import get_user_model

User = get_user_model()



class ReportService:

    @staticmethod
    def get_daily_attendance():
        today = timezone.now().date()

        attendances = Attendance.objects.filter(date=today).select_related("user")

        return {
            "date": today,
            "total_check_ins": attendances.count(),
            "attendees": [
                {
                    "user_id": att.user.id,
                    "username": att.user.username,
                    "check_in_time": att.check_in_time
                }
                for att in attendances
            ]
        }
    @staticmethod
    def get_revenue_report():
        memberships = Membership.objects.select_related("plan")
        day_passes = DayPass.objects.all()

        membership_revenue = sum(m.plan.price for m in memberships)
        daypass_revenue = sum(dp.price for dp in day_passes)

        return {
            "membership_revenue": membership_revenue,
            "daypass_revenue": daypass_revenue,
            "total_revenue": membership_revenue + daypass_revenue
        }
    
    @staticmethod
    def get_active_members():
        active_users = User.objects.filter(is_active=True)

        return {
            "total_active_members": active_users.count(),
            "members": [
                {
                    "id": user.id,
                    "username": user.username
                }
                for user in active_users
            ]
        }
    
    @staticmethod
    def get_membership_status():
        memberships = Membership.objects.all()

        active_count = 0
        expired_count = 0

        for membership in memberships:
            if membership.is_valid():
                active_count += 1
            else:
                expired_count += 1

        return {
            "total_memberships": memberships.count(),
            "active_memberships": active_count,
            "expired_memberships": expired_count
        }