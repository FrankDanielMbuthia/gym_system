from rest_framework import serializers

class ActivateMembershipSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    plan_id = serializers.IntegerField()