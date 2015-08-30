from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.models import UserInfo
from services.serializers import *
from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'buildings': reverse('building-list', request=request, format=format),
        'boards': reverse('board-list', request=request, format=format),
        'beaconArounds': reverse('beaconAround-list', request=request, format=format),
        'usersInfo': reverse('userInfo-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format),
        'samples': reverse('sample-list', request=request, format=format),
        'sampleDescriptors': reverse('sampleDescriptor-list', request=request, format=format)
    })

class BuildingList(generics.ListCreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BuildingDetail(generics.RetrieveUpdateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BoardDetail(generics.RetrieveUpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BeaconAroundList(generics.ListCreateAPIView):
    queryset = BeaconAround.objects.all()
    serializer_class = BeaconAroundSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BeaconAroundDetail(generics.RetrieveUpdateAPIView):
    queryset = BeaconAround.objects.all()
    serializer_class = BeaconAroundSerializer

class UserInfoList(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserInfoDetail(generics.RetrieveAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class SampleList(generics.ListCreateAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SampleDetail(generics.RetrieveAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer

class SampleDescriptorList(generics.ListCreateAPIView):
    queryset = SampleDescriptor.objects.all()
    serializer_class = SampleDescriptorSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SampleDescriptorDetail(generics.RetrieveAPIView):
    queryset = SampleDescriptor.objects.all()
    serializer_class = SampleDescriptorSerializer

def test(request):
    userinfos = UserInfo.objects.all()
    return HttpResponse(str(userinfos[0].__dict__))