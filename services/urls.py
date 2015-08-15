from django.conf.urls import url
from services import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^building/$', views.Building_list),
    url(r'^building/(?P<pk>[0-9]+)/$', views.Building_detail),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)