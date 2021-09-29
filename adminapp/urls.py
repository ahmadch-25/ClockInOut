from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import AdminPanel,AddEmployee,EditEmployee,DeleteEmployee,logoutadmin,adminettings

urlpatterns = [
    path('', AdminPanel,name="adminapp-panel"),
    path('addemploye/',AddEmployee,name='addemployee'),
    path('editemploye/<int:pk>',EditEmployee,name='editemploye'),
    path('deleteemploye/<int:pk>',DeleteEmployee,name='deleteemplaoyee'),
    path('logoutadmin',logoutadmin,name='logoutadmin'),
    path('adminettings',adminettings,name="adminettings")
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)