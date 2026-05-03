from django.urls import path
from .views import DailyAttendanceReportView, RevenueReportView, ActiveMembersReportView, MembershipStatusReportView

urlpatterns = [
    path("attendance/daily/", DailyAttendanceReportView.as_view()),
    path("revenue/", RevenueReportView.as_view()),
    path("members/active/", ActiveMembersReportView.as_view()),
    path("memberships/status/", MembershipStatusReportView.as_view()),
]