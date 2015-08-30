from django.conf.urls import url
from services import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^buildings/$', views.BuildingList.as_view(), name='building-list'),
    url(r'^buildings/(?P<pk>[0-9]+)/$', views.BuildingDetail.as_view(), name='building-detail'),
    url(r'^boards/$', views.BoardList.as_view(), name='board-list'),
    url(r'^boards/(?P<pk>[0-9]+)/$', views.BoardDetail.as_view(), name='board-detail'),
    url(r'^beaconArounds/$', views.BeaconAroundList.as_view(), name='beaconAround-list'),
    url(r'^beaconArounds/(?P<pk>[0-9]+)/$', views.BeaconAroundDetail.as_view(), name='beaconAround-detail'),
    url(r'^usersInfo/$', views.UserInfoList.as_view(), name='userInfo-list'),
    url(r'^usersInfo/(?P<pk>[0-9]+)/$', views.UserInfoDetail.as_view(), name='userInfo-detail'),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^orders/$', views.OrderList.as_view(), name='order-list'),
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderDetail.as_view(), name='order-detail'),
    url(r'^samples/$', views.SampleList.as_view(), name='sample-list'),
    url(r'^samples/(?P<pk>[0-9]+)/$', views.SampleDetail.as_view(), name='sample-detail'),
    url(r'^sampleDescriptors/$', views.SampleDescriptorList.as_view(), name='sampleDescriptor-list'),
    url(r'^sampleDescriptors/(?P<pk>[0-9]+)/$', views.SampleDescriptorDetail.as_view(), name='sampleDescriptor-detail'),
    url(r'^test/$', views.test),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
urlpatterns = format_suffix_patterns(urlpatterns)
