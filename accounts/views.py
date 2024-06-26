from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *
from complaints.models import Employee,Department,Category

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
    def check_password(self,password):
        if len(password) < 8:
            return False
        
        has_number = any(char.isdigit() for char in password)
        return has_number
    
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
        des = request.POST.get("des")
        
        if password != password2:
            err = "Password not matching!"
            return redirect(f"/accounts/signup?err={err}")
        
        if not self.check_password(password):
            err = "Password must have 8 characters and atleast 1 letter!"
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
                                     address=address,country=country,state=state,
                                     user_type=user_type,des=des)
        
        if user_type == 'GOV_EMPLOYEE':
            Employee.objects.create(user=acc)

        return redirect('/accounts/login')
        
    
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("/accounts/login/")
    

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        emp = None
        if acc.user_type == 'GOV_EMPLOYEE':
            emp = Employee.objects.filter(user=acc).last()
        return render(request,'profile.html',{'acc':acc,'emp':emp})
    


@method_decorator(login_required,name='dispatch')
class EditProfileView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        emp = None
        dept = None
        category = None

        if acc.user_type == 'GOV_EMPLOYEE':
            emp = Employee.objects.filter(user=acc).last()
            dept = Department.objects.all()
            category = Category.objects.all()
        return render(request,'edit_profile.html',{'acc':acc,'emp':emp,'dept':dept,'category':category})
    

    def post(self,request):
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")
        address = request.POST.get("address")
        department_id = request.POST.get("dept")
        category_id = request.POST.get("category")

        acc = Account.objects.get(user=request.user)
        emp = Employee.objects.filter(user=acc).last()

        dept = Department.objects.get(id=department_id)
        # category = Category.objects.get(id=category_id)

        acc.full_name = full_name
        acc.email = email
        acc.phone = phone
        acc.address = address
        acc.pincode = pincode

        if acc.user_type == 'GOV_EMPLOYEE':
            # emp.category = category
            emp.department = dept
            emp.save()

        acc.save()

        return redirect("/accounts/profile")