from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class BuildingSerializer(serializers.HyperlinkedModelSerializer):
    boards = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='board-detail')

    class Meta:
        model = Building
        fields = ('url', 'id', 'mapUrl', 'mapScale', 'latitude', 'longitude', 'description', 'creationTime', 'boards')


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    orderDetail = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='order-detail')

    class Meta:
        model = Board
        fields = ('url', 'boardIdentity', 'ownerBuilding', 'isCovered', 'orderDetail', 'coordinateX', 'coordinateY',
                  'command', 'description')


class BeaconAroundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BeaconAround


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    # orders = OrderSerializer(many=True)
    orders = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='order-detail')
    # parkingUser = serializers.PrimaryKeyRelatedField(many=True, queryset=UserInfo.objects.all())
    # user = serializers.ReadOnlyField(source='user.url')
    is_staff = serializers.ReadOnlyField(source='user.is_staff')
    is_active = serializers.ReadOnlyField(source='user.is_active')
    # date_joined = serializers.ReadOnlyField(source='user.date_joined')
    # user = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='user-detail')
    user_name = serializers.ReadOnlyField(source='user.username')
    groups = serializers.StringRelatedField(many=True, source='user.groups')

    class Meta:
        model = UserInfo
        fields = (
            'url', 'user_name', 'uuid', 'major_Id', 'minor_Id', 'mac_address', 'creation_Time', 'orders', 'is_staff',
            'is_active', 'groups')
        # {'user_id': 1, 'minor_Id': u'03', 'major_Id': u'02', '_state': , 'mac_address': u'111111', 'creation_Time': datetime.datetime(2015, 8, 18, 14, 4, 56, 272389, tzinfo=), 'id': 1, 'uuid': u'2f234454cf6d4a0fadf2f4911ba9ffa6'}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # groups = serializers.ReadOnlyField(source='groups')
    groups = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'is_staff', 'is_active', 'date_joined', 'groups')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    # owner below is like a re-mapping property 'owner' for Order, so means the Order must have 'owner' property first.
    # owner = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='userinfo-detail')
    owner_uuid = serializers.ReadOnlyField(source='owner.uuid')
    owner_majorId = serializers.ReadOnlyField(source='owner.major_Id')
    owner_minorId = serializers.ReadOnlyField(source='owner.minor_Id')

    class Meta:
        model = Order
        fields = ('url', 'owner', 'owner_uuid', 'owner_majorId', 'owner_minorId', 'status', 'to_Board', 'isActive',
                  'creation_Time')


class SampleSerializer(serializers.HyperlinkedModelSerializer):
    # owner below is like a re-mapping property 'ownerBuilding' for Order, so means the Order must have 'ownerBuilding' property first.
    ownerBuilding = serializers.HyperlinkedRelatedField(many=False, required=True, queryset=Building.objects.all(),
                                                        view_name='building-detail')
    sampleDescriptors = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                            view_name='sampledescriptor-detail')

    class Meta:
        model = Sample
        fields = (
            'url', 'ownerBuilding', 'sampleDescriptors', 'coordinateX', 'coordinateY', 'creation_Time', 'description')


class SampleDescriptorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SampleDescriptor
        fields = (
            'url', 'ownerSample', 'uuid', 'major_Id', 'minor_Id', 'mac_address', 'tx_value', 'rssi_value',
            'caculated_distance',
            'creation_Time')
