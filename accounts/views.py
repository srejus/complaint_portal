from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *

# Create your views here.

class LoginView(View):
    def get(self,request):
        err = request.GET.get("err")
        type_ = request.GET.get("type_","User")
        return render(request,'login.html',{'err':err,'type_':type_})

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")

        print('User type : ',user_type)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:            
            acc = Account.objects.get(user=user)
            print("DATA : ",acc.user_type )
            if user_type == 'user' and acc.user_type == 'USER':
                login(request, user)
                next = request.GET.get("next")
                if next:
                    return redirect(next)
                return redirect("/")
            
            if user_type == 'employee' and acc.user_type == 'GOV_EMPLOYEE':
                login(request, user)
                next = request.GET.get("next")
                if next:
                    return redirect(next)
                return redirect("/")
        
            if user_type == 'admin' and acc.user_type == 'ADMIN':
                login(request, user)
                next = request.GET.get("next")
                if next:
                    return redirect(next)
                return redirect("/")

        err = "Invalid credentails!"
        return redirect(f"/accounts/login/?err={err}")
    

class SignupView(View):
    def get(self,request):
        err = request.GET.get("err")
        return render(request,'signup.html',{'err':err})
    
    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")
        state = request.POST.get("state")
        country = request.POST.get("country")
        address = request.POST.get("address")
        user_type = request.POST.get("user_type")
        
        if password != password2:
            err = "Password not matching!"
            return redirect(f"/accounts/signup?err={err}")
    
        user = User.objects.filter(username=username)
        if user.exists():
            err = "User with this username already exists"
            return redirect(f"/accounts/signup?err={err}")
        
        acc = Account.objects.filter(Q(email=email) | Q(phone=phone)).exists()
        if acc:
            err = "User with this phone or email already exists"
            return redirect(f"/accounts/signup?err={err}")
        
        user = User.objects.create_user(username=username,email=email,password=password)
        acc = Account.objects.create(user=user,full_name=full_name,
                                     phone=phone, email=email,pincode=pincode,
                                     address=address,country=country,state=state,user_type=user_type)

        return redirect('/accounts/login')
        
    