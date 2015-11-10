from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.models import UserInfo
from .models import Document
from .forms import DocumentForm
from services.serializers import *
from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from services.permissions import *
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
import os


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'buildings': reverse('building-list', request=request, format=format),
        'boards': reverse('board-list', request=request, format=format),
        'beaconArounds': reverse('beaconAround-list', request=request, format=format),
        'usersInfo': reverse('userinfo-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format),
        'samples': reverse('sample-list', request=request, format=format),
        'sampledescriptors': reverse('sampledescriptor-list', request=request, format=format)
    })


class BuildingList(generics.ListCreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    # only technician can add new build, other (even anonymous user can check it)
    permission_classes = (IsTechniciansGroupOrReadOnly,)
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class BuildingDetail(generics.RetrieveUpdateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = (IsTechniciansGroupOrReadOnly,)


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated, IsRobotsGroupOrReadOnly)

    def get_queryset(self):
        queryset = Board.objects.all()
        ownerBuildingId = self.request.query_params.get('ownerBuildingId', None)

        if ownerBuildingId is not None:
            queryset = queryset.filter(ownerBuilding=ownerBuildingId)

        return queryset
        # def perform_create(self, serializer):
        #     serializer.save(owner=self.request.user)


class BoardDetail(generics.RetrieveUpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated, IsRobotsGroupOrReadOnly)


class BeaconAroundList(generics.ListCreateAPIView):
    queryset = BeaconAround.objects.all()
    serializer_class = BeaconAroundSerializer

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class BeaconAroundDetail(generics.RetrieveUpdateAPIView):
    queryset = BeaconAround.objects.all()
    serializer_class = BeaconAroundSerializer


class UserInfoList(generics.ListCreateAPIView):
    # queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # for superUsers Group, list all users, otherwise, only list the current authenticated user information.
        if self.request.user.groups.filter(name='SuperUsers').exists():
            return UserInfo.objects.all()
        else:
            return UserInfo.objects.filter(user=self.request.user)

        # def list(self, request):
        #     # Note the use of `get_queryset()` instead of `self.queryset`
        #     queryset = self.get_queryset()
        #     serializer = UserSerializer(queryset, many=True)
        #     return Response(serializer.data)


class UserInfoDetail(generics.RetrieveAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated, IsUserInfoSelfOrDeny)


class UserList(generics.ListCreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUsersGroupOrDeny)

    def get_queryset(self):
        # for superUsers Group, list all users, otherwise, only list the current authenticated user information.
        if self.request.user.groups.filter(name='SuperUsers').exists():
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUsersGroupOrDeny)


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDeny)

    def get_queryset(self):
        queryset = Order.objects.all()
        ownerUserInfoId = self.request.query_params.get('ownerUserInfoId', None)
        to_BoardId = self.request.query_params.get('to_BoardId', None)
        if ownerUserInfoId is not None:
            queryset = queryset.filter(owner=ownerUserInfoId)

        if to_BoardId is not None:
            queryset = queryset.filter(to_Board=to_BoardId)
        return queryset
        # def perform_create(self, serializer):
        #     newUserInfo = UserInfo()
        #     newUserInfo.user = self.request.user
        #     serializer.save(owner=newUserInfo)


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDeny)


class SampleList(generics.ListCreateAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = (permissions.IsAuthenticated, IsTechniciansGroupOrReadOnly,)

    def get_queryset(self):
        queryset = Sample.objects.all()
        ownerBuildingId = self.request.query_params.get('ownerBuildingId', None)
        _coordinateX = self.request.query_params.get('coordinateX', None)
        _coordinateY = self.request.query_params.get('coordinateY', None)
        if ownerBuildingId is not None:
            if _coordinateX is not None and _coordinateY is not None:
                queryset = queryset.filter(ownerBuilding=ownerBuildingId).filter(coordinateX=_coordinateX).filter(
                    coordinateY=_coordinateY)
            queryset = queryset.filter(ownerBuilding=ownerBuildingId)

        return queryset
        # def get_serializer(self, instance=None, data=None, many=False, partial=False):
        #     return super(generics.ListCreateAPIView, self).get_serializer(many=True, partial=False)


class SampleDetail(generics.RetrieveAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = (permissions.IsAuthenticated, IsTechniciansGroupOrReadOnly,)


class SampleDescriptorList(generics.ListCreateAPIView):
    queryset = SampleDescriptor.objects.all()
    serializer_class = SampleDescriptorSerializer
    permission_classes = (permissions.IsAuthenticated, IsTechniciansGroupOrReadOnly,)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class SampleDescriptorDetail(generics.RetrieveAPIView):
    queryset = SampleDescriptor.objects.all()
    serializer_class = SampleDescriptorSerializer
    permission_classes = (permissions.IsAuthenticated, IsTechniciansGroupOrReadOnly,)


def test0(request):
    userinfos = User.objects.all()
    gggg = userinfos[0].groups
    # result = ""
    # for g in gggg:
    #     result +=str(g.__dict__)+"-------"
    return HttpResponse(str(gggg[0].__dict__))
    # return HttpResponse(str(gggg[0].__dict__) + "----------" + str(userinfos[1].__dict__)+ "----------" + str(userinfos[2].__dict__)+ "----------" + str(userinfos[3].__dict__)+ "----------" + str(userinfos[4].__dict__))


def test1(request):
    groups = Group.objects.all()
    return HttpResponse(
        str(groups[0].__dict__) + "----------" + str(groups[1].__dict__) + "----------" + str(groups[2].__dict__))


# ====================== upload files =========================

def uploadFiles(request):
    # Load documents for the list page
    documents = Document.objects.all()
    # if request.method == 'GET':
    #     returnStr = ""
    #     # return HttpResponse(str(documents[0].__dict__))
    #     for d in documents:
    #         returnStr += d.docfile.url + "</br>"
    #     return HttpResponse(returnStr)

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        # 100 px equal how many real life meters, like say the value is 5, means
        # 100px in bitmap equal 5meters, default set to 2.
        # mapscale = request.POST["mapScale"]
        if form.is_valid():
            # return render_to_response("pending to save")
            newdoc = Document(docfile=request.FILES['docfile'])  # , mapscale=mapscale)
            # newdoc.mapscale = mapscale
            newdoc.save()
            # return HttpResponse(str(newdoc.__dict__))
            # handle_uploaded_file(request.FILES['file'])
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('services.views.uploadFiles'))
    else:
        form = DocumentForm()  # A empty, unbound form
    # Render list page with the documents and the form
    return render_to_response(
        'services/uploadFile.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


def displayalluploadedfilesurl(request):
    # Load documents for the list page
    documents = Document.objects.all()


def handle_uploaded_file(f):
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def deleteUploadedFile(request):
    fileName = request.GET.get("filename")
    if not fileName:
        raise Exception(
            "need provide the filename for deleting")
    targetFile = Document.objects.get(docfile=fileName)
    targetFile.delete()
    # allFiles = Document.objects.get(docfile=filename)
    # logStr = ""
    # for oneFile in allFiles:
    # logStr += settings.MEDIA_ROOT + str(oneFile.docfile) + "</br>"
    os.remove('/var/www/upload/' + fileName)
    return HttpResponse("Delete: " + fileName + " succeed")
