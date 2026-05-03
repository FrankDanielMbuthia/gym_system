from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .services import ReportService


class DailyAttendanceReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = ReportService.get_daily_attendance()
        return Response(data)
    
class RevenueReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = ReportService.get_revenue_report()
        return Response(data)
    
class ActiveMembersReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = ReportService.get_active_members()
        return Response(data)
    
class MembershipStatusReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = ReportService.get_membership_status()
        return Response(data)