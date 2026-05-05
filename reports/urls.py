from django.urls import path
from .views import (DailyAttendanceView, RevenueReportView, ActiveMembersView, MembershipStatusView)

urlpatterns = [
    path("attendance/daily/", DailyAttendanceView.as_view()),
    path("revenue/", RevenueReportView.as_view()),
    path("active-members/", ActiveMembersView.as_view()),
    path("membership-status/", MembershipStatusView.as_view()),
]