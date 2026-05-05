from django.urls import path
from .views import ActivateMembershipView, MembershipPlanListView, MyMembershipView

urlpatterns = [
    path("activate/", ActivateMembershipView.as_view(), name="activate-membership"),
    path("plans/", MembershipPlanListView.as_view()),
    path("my/", MyMembershipView.as_view()),
]