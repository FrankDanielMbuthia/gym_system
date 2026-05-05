from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .services import ReportService


class DailyAttendanceView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(ReportService.get_daily_attendance())


class RevenueReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(ReportService.get_revenue())


class ActiveMembersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(ReportService.get_active_members())


class MembershipStatusView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(ReportService.get_membership_status())