from django.utils import timezone
from attendance.models import Attendance, DayPass
from memberships.models import Membership
from django.db.models import Sum


class ReportService:

    @staticmethod
    def get_daily_attendance():
        today = timezone.now().date()

        attendances = Attendance.objects.filter(date=today)

        member_count = attendances.filter(user__isnull=False).count()
        day_pass_count = attendances.filter(day_pass__isnull=False).count()

        return {
            "date": str(today),
            "members": member_count,
            "day_pass_users": day_pass_count,
            "total": member_count + day_pass_count
        }

    @staticmethod
    def get_revenue():
        membership_revenue = Membership.objects.aggregate(
            total=Sum("plan__price")
        )["total"] or 0

        day_pass_revenue = DayPass.objects.aggregate(
            total=Sum("price")
        )["total"] or 0

        return {
            "membership_revenue": membership_revenue,
            "day_pass_revenue": day_pass_revenue,
            "total_revenue": membership_revenue + day_pass_revenue
        }

    @staticmethod
    def get_active_members():
        today = timezone.now().date()

        active_memberships = Membership.objects.filter(
            start_date__date__lte=today,
            end_date__date__gte=today
        )

        active_users = [m.user for m in active_memberships]

        return {
            "total_active_members": len(active_users),
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
        today = timezone.now().date()
    
        active_memberships = Membership.objects.filter(
            start_date__date__lte=today,
            end_date__date__gte=today
        )
    
        expired_memberships = Membership.objects.filter(
            end_date__date__lt=today
        )
    
        return {
            "active_count": active_memberships.count(),
            "expired_count": expired_memberships.count(),
    
            "active_members": [
                {
                    "id": m.user.id,
                    "username": m.user.username,
                    "plan": m.plan.name,
                    "end_date": m.end_date
                }
                for m in active_memberships
            ],
    
            "expired_members": [
                {
                    "id": m.user.id,
                    "username": m.user.username,
                    "plan": m.plan.name,
                    "end_date": m.end_date
                }
                for m in expired_memberships
            ]
        }