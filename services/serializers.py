from rest_framework import serializers
from .models  import *
class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('pk', 'description', 'mapUrl', 'creationTime')

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        #fields = ()


class BeaconAroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeaconAround


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class OrderSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Order

