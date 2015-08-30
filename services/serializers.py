from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class BuildingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Building
        fields = ('pk', 'description', 'mapUrl', 'creationTime')


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        # fields = ()


class BeaconAroundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BeaconAround


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    # orders = OrderSerializer(many=True)
    orders = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='order-detail')
    # parkingUser = serializers.PrimaryKeyRelatedField(many=True, queryset=UserInfo.objects.all())
    # user = serializers.ReadOnlyField(source='user.url')
    # is_staff = serializers.ReadOnlyField(source='user.is_staff')
    # is_active = serializers.ReadOnlyField(source='user.is_active')
    # date_joined = serializers.ReadOnlyField(source='user.date_joined')
    user = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='user-detail')

    class Meta:
        model = UserInfo
        fields = ('user', 'uuid', 'major_Id', 'minor_Id', 'mac_address', 'creation_Time', 'orders')
        # {'user_id': 1, 'minor_Id': u'03', 'major_Id': u'02', '_state': , 'mac_address': u'111111', 'creation_Time': datetime.datetime(2015, 8, 18, 14, 4, 56, 272389, tzinfo=), 'id': 1, 'uuid': u'2f234454cf6d4a0fadf2f4911ba9ffa6'}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'is_active', 'date_joined')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    # owner below is like a re-mapping property 'owner' for Order, so means the Order must have 'owner' property first.
    owner = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='userInfo-detail')

    class Meta:
        model = Order


class SampleSerializer(serializers.HyperlinkedModelSerializer):
    # owner below is like a re-mapping property 'ownerBuilding' for Order, so means the Order must have 'ownerBuilding' property first.
    ownerBuilding = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='building-detail')
    sampleDescriptors = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='sampleDescriptor-detail')
    class Meta:
        model = Sample
        fields = ('ownerBuilding', 'sampleDescriptors', 'coordinateX', 'coordinateY', 'creation_Time')

class SampleDescriptorSerializer(serializers.HyperlinkedModelSerializer):
    # owner below is like a re-mapping property 'ownerSample' for ownerSample, so means the Order must have 'ownerSample' property first.
    ownerSample = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='sample-detail')

    class Meta:
        model = SampleDescriptor
        fields = ('ownerSample', 'uuid', 'major_Id', 'minor_Id', 'mac_address','tx_value','rssi_value','caculated_distance', 'creation_Time')