from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import userpanel,home,logoutuser,ajaxrequest,usersettings

urlpatterns = [
    path('userpanel', userpanel,name="userpanel"),
    path('',home,name="user-home"),
    path("logoutuser",logoutuser,name='logout'),
    path("ajaxrequest",ajaxrequest,name="ajaxrequest"),
    path("usersettings",usersettings,name="usersettings"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)