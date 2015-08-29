from rest_framework import serializers
from .models  import *
from django.contrib.auth.models import User
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

class UserInfoSerializer(serializers.ModelSerializer):
    #orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())
    #orders = serializers.ReadOnlyField(source='orders.status')
    #parkingUser = serializers.PrimaryKeyRelatedField(many=True, queryset=UserInfo.objects.all())
    class Meta:
        model = User
        fields = ('id','parkingUser', 'orders','username','is_staff','is_active','date_joined','groups','user_permissions')
        #{'user_id': 1, 'minor_Id': u'03', 'major_Id': u'02', '_state': , 'mac_address': u'111111', 'creation_Time': datetime.datetime(2015, 8, 18, 14, 4, 56, 272389, tzinfo=), 'id': 1, 'uuid': u'2f234454cf6d4a0fadf2f4911ba9ffa6'}

class OrderSerializer(serializers.ModelSerializer):
    # owner below is like a re-mapping property 'owner' for Order, so means the Order must have 'owner' property first.
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Order

class SampleSerializer(serializers.ModelSerializer):
    # owner below is like a re-mapping property 'ownerBuilding' for Order, so means the Order must have 'ownerBuilding' property first.
    ownerBuilding = serializers.ReadOnlyField(source='ownerBuilding.mapUrl')
    class Meta:
        model = Sample

class SampleDescriptorSerializer(serializers.ModelSerializer):
    # owner below is like a re-mapping property 'ownerSample' for ownerSample, so means the Order must have 'ownerSample' property first.
    ownerSample = serializers.ReadOnlyField(source='ownerSample.ownerBuilding.mapUrl')
    class Meta:
        model = SampleDescriptor