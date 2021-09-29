"""ClockInOut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from Users.views import home
from adminapp.views import afterlogin_view

urlpatterns = [
    path('superuser/',admin.site.urls),
    path('adminlogin', LoginView.as_view(template_name='adminapp/login.html'),name='adminlogin'),
    path('userlogin', LoginView.as_view(template_name='login.html'),name='userlogin'),
    path('admin/', include('adminapp.urls'), name="adminapp"),
    path('afterlogin', afterlogin_view,name='afterlogin'),
    path('',include('Users.urls'),name='users'),
    #path('logout',home,name='logout'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
