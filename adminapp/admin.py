from django.contrib import admin
from .models import Employee,Report

# Register your models here.


@admin.register(Employee)
class EmployeeAdmoin(admin.ModelAdmin):
    list_display = ['id', 'user', 'login_session', 'is_active', 'created_at']
#admin.site.register(Employee)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [feilds.name for feilds in Report._meta.get_fields()]