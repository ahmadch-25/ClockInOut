from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from adminapp.models import Report,Employee
from django.contrib.auth.models import User
import datetime
from django.contrib import messages
from django.http import JsonResponse

def is_employee(user):
    return user.groups.filter(name='employee').exists()


@login_required(login_url='userlogin')
@user_passes_test(is_employee,login_url='userlogin')
def userpanel(request):
    employe = Employee.objects.get(user=request.user)
    last_record = Report.objects.filter(user_id=employe).order_by("-started_at").first()
    print(last_record)
    if last_record:
        context={"started_at":last_record.started_at,"ended_at":last_record.ended_at}
    else:
        context = {"started_at": "", "ended_at": ""}
    context["user"]=request.user
    return render(request,"panel.html",context)


@login_required(login_url='userlogin')
@user_passes_test(is_employee,login_url='userlogin')
def usersettings(request):
    context={"user":request.user}
    if request.method=="POST":
        data=request.POST
        if User.objects.filter(username=data["username"]).exists():
            messages.success(request, "Username Already Exist")
            return render(request, "settings.html", context)
        user=User.objects.get(username=request.user.username)
        user.username=data["username"]
        if data["password"]!="":
            user.set_password(data["password"])
        user.save()
        context={"user":user}
        messages.success(request, "User updated Successfully")
        return render(request, "settings.html", context)
    return render(request,"settings.html",context)



def home(request):
    list_display = [feilds.name for feilds in Employee._meta.get_fields()]
    print(list_display)
    date=datetime.datetime.now()
    print(date)
    date=date.strftime("%Y-%m-%d %H:%M:%S")
    #date=datetime.datetime.strptime(str(date),)
    print(date)
    if request.user.is_anonymous:
        user_login=False
    else:
        if is_employee(request.user):
            user_login=True
        else:
            user_login=False
    context={"is_user_login":user_login,"date":date}
    return render(request,"Home.html",context)


@login_required(login_url='userlogin')
@user_passes_test(is_employee,login_url='userlogin')
def logoutuser(request):
    logout(request)
    return redirect(home)

def check_isuserlogin(request):
    if request.user.is_anonymous:
        user_login=False
    else:
        if is_employee(request.user):
            user_login=True
        else:
            user_login=False
    return user_login


def ajaxrequest(request):
    data=request.POST
    print(check_isuserlogin(request))
    if check_isuserlogin(request):
        employe = Employee.objects.filter(user=request.user).first()
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        last_record = Report.objects.filter(user_id=employe).order_by("-started_at").first()
        if "clock_in" in data:
            if last_record and last_record.ended_at == None:
                response = {"message": ["It should be clock out"], "success": False}
                return JsonResponse(response)
            else:
                report = Report(user_id=employe, started_user_local_time=data["userLocalTime"])
                report.save()
                response = {"message": ["Clock In at <b>" + date[11:17] + "</b>"], "success": True,"date":date,"clock_in":True}
                return JsonResponse(response)
        if "clock_out" in data:
            if last_record==None or last_record.ended_at != None:
                response = {"message": ["It should be clock In"], "success": False}
                return JsonResponse(response)
            else:
                last_record.ended_at = date
                last_record.ended_user_local_time = data["userLocalTime"]
                last_record.save()
                response = {"message": ["Clock Out at <b>" + date[11:17] + "</b>"], "success": True,"date":date,"clock_in":False}
                return JsonResponse(response)
        response = {"message": ["An error has been occurred. Please try it later"], "success": False}
        return JsonResponse(response)
    else:
        user=User.objects.filter(username=data['username']).first()
        employe=Employee.objects.filter(user=user).first()
        if employe:
            if user.check_password(data['password']):
                date = datetime.datetime.now()
                date = date.strftime("%Y-%m-%d %H:%M:%S")
                last_record=Report.objects.filter(user_id=employe).order_by("-started_at").first()
                if "clock_in" in data:
                    if last_record and last_record.ended_at==None:
                        response = {"message": ["It should be clock out"], "success": False}
                        return JsonResponse(response)
                    else:
                        report=Report(user_id=employe,started_user_local_time=data["userLocalTime"])
                        report.save()
                        response = {"message": ["Clock In at <b>" + date[11:17] + "</b>"], "success": True}
                        return JsonResponse(response)
                if "clock_out" in data:
                    if last_record==None or last_record.ended_at != None:
                        response = {"message": ["It should be clock In"], "success": False}
                        return JsonResponse(response)
                    else:
                        last_record.ended_at=date
                        last_record.ended_user_local_time=data["userLocalTime"]
                        last_record.save()
                        response = {"message": ["Clock Out at <b>" + date[11:17] + "</b>"], "success": True}
                        return JsonResponse(response)
                response={"message":["ok"],"success":True}
                return JsonResponse(response)
            else:
                response = {"success": False, "message": ["Password not correct"]}
                return JsonResponse(response)
        else:
            response={"success":False,"message":["Username not correct"]}
            return JsonResponse(response)