from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_session=models.CharField(max_length=100,verbose_name='Login Session',blank=True,null=True)
    is_active = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_username(self):
        return self.user.username

    @property
    def get_id(self):
        return self.id

    def __str__(self):
        return str(self.id)+"   -   "+self.user.username

    class Meta:
        verbose_name="Employee"
        verbose_name_plural="Employees"


class Report(models.Model):
    user_id = models.ForeignKey(Employee,on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    started_user_local_time = models.CharField(max_length=100)
    ended_at = models.DateTimeField(null=True,blank=True)
    ended_user_local_time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.id)+"   "+self.user_id.user.username

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'


