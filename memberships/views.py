from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from .serializers import ActivateMembershipSerializer
from .services import MembershipService


class ActivateMembershipView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ActivateMembershipSerializer(data=request.data)

        if serializer.is_valid():
            MembershipService.activate_membership(
                user_id=serializer.validated_data["user_id"],
                plan_id=serializer.validated_data["plan_id"]
            )

            return Response(
                {"message": "Membership activated successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)