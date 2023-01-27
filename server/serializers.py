from .models import EGridPlant
from rest_framework import serializers


class EGridPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EGridPlant
        fields = '__all__'