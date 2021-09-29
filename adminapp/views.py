from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from adminapp.forms import UserForm
from .models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from Users.views import userpanel
from django.core.paginator import Paginator
# Create your views here.

def is_admin(user):
    return user.groups.filter(name='admin').exists()


@login_required(login_url='adminlogin')
@user_passes_test(is_admin,login_url='adminlogin')
def AdminPanel(request):
    employee=Employee.objects.all()
    paginator = Paginator(employee, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'employes': employee, "user": request.user,'page_obj': page_obj}
    return render(request, "adminapp/admin.html",context)



def is_employee(user):
    return user.groups.filter(name='employee').exists()



def assign_user_group(user):
    my_group = Group.objects.get(name='employee')
    my_group.user_set.add(user)


def afterlogin_view(request):
    if is_employee(request.user):
        return redirect(userpanel)
    else:
        print("admin")
        return redirect('admin')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin,login_url='adminlogin')
def AddEmployee(request):
    userform=UserForm()
    if request.method=="POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            user=userform.save()
            user.set_password(user.password)
            user.save()
            assign_user_group(user)
            employee=Employee()
            employee.user=user
            employee.save()
            messages.success(request, "user added successfully")
            return redirect('/admin')
    context={"userform":userform}
    return render(request,"adminapp/employe_add.html",context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin,login_url='adminlogin')
def EditEmployee(request,pk):
    employee=Employee.objects.get(id=pk);
    userform=UserForm(instance=employee.user)
    if request.method=="POST":
        userform = UserForm(request.POST,instance=employee.user)
        if userform.is_valid():
            user=userform.save()
            if userform.instance.password!="default":
                user.set_password(user.password)
            user.save()
            messages.success(request, "user updated successfully")
            return redirect('/admin')
    context={"userform":userform}
    return render(request,"adminapp/employe_edit.html",context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin,login_url='adminlogin')
def DeleteEmployee(request,pk):
    user=User.objects.get(id=pk)
    user.delete()
    messages.success(request,"user deleted successfully")
    return redirect('/admin')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin,login_url='adminlogin')
def adminettings(request):
    context={"user":request.user}
    if request.method=="POST":
        data=request.POST
        if User.objects.filter(username=data["username"]).exists():
            messages.success(request, "Username Already Exist")
            return render(request, "adminapp/settings.html", context)
        user=User.objects.get(username=request.user.username)
        user.username=data["username"]
        if data["password"]!="":
            user.set_password(data["password"])
        user.save()
        context={"user":user}
        messages.success(request, "User updated Successfully")
        return render(request, "adminapp/settings.html", context)
    return render(request,"adminapp/settings.html",context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin,login_url='adminlogin')
def logoutadmin(request):
    logout(request)
    return redirect(AdminPanel)