from django.urls import path
from .views import CheckInView, DayPassCreateView, TodayAttendanceView

urlpatterns = [
    path("check-in/", CheckInView.as_view(), name="check-in"),
    path("day-pass/", DayPassCreateView.as_view()),
    path("today/", TodayAttendanceView.as_view()),
]   