from django.urls import path
from .views import ActivateMembershipView

urlpatterns = [
    path("activate/", ActivateMembershipView.as_view(), name="activate-membership"),
]