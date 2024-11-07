from rest_framework import serializers

from .models import Computer


class ComputerSerializer(serializers.ModelSerializer):
    softwares = serializers.StringRelatedField(many=True)
    class Meta:
        model = Computer
        fields = ["device_uid", "softwares"]

