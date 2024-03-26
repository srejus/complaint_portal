from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from accounts.models import Account
from complaints.models import Employee,Complaint,Category,Department

# Create your views here.

def is_hr_user(request):
    acc = Account.objects.get(user=request.user)
    if acc.user_type == 'ADMIN':
        return True
    return False

@method_decorator(login_required, name='dispatch')
class HrHomeView(View):
    def get(self,request):
        if not is_hr_user(request):
            return redirect("/")
        
        return render(request,'hr_dashboard.html')
    

@method_decorator(login_required, name='dispatch')
class HrComplaintsView(View):
    def get(self,request,id=None):
        if not is_hr_user(request):
            return redirect("/")
        
        complaints = Complaint.objects.all().order_by('-id')
        if id:
            complaints = complaints.filter(id=id).first()
            return render(request,'view_compliant_hr.html',{'complaint':complaints})
        return render(request,'hr_complaints.html',{'complaints':complaints})
    
    def post(self,request,id):
        reply = request.POST.get("reply")
        status = request.POST.get("status")
        compliant = Complaint.objects.get(id=id)
        if reply:
            compliant.hr_response = reply
        if status != 'NA':
            compliant.status = status
        compliant.hr_response_added_at = timezone.now()
        compliant.save()
        return redirect(f"/hr/{id}")
    

@method_decorator(login_required, name='dispatch')
class HrEmployeesView(View):
    def get(self,request):
        if not is_hr_user(request):
            return redirect("/")
        
        employees = Employee.objects.all()
        return render(request,'hr_employees.html',{'employees':employees})
    



@method_decorator(login_required, name='dispatch')
class HrCategoryView(View):
    def get(self,request):
        if not is_hr_user(request):
            return redirect("/")
        
        category = Category.objects.all()
        return render(request,'hr_category.html',{'category':category})
    


@method_decorator(login_required, name='dispatch')
class HrDepartmentView(View):
    def get(self,request):
        if not is_hr_user(request):
            return redirect("/")
        
        department = Department.objects.all()
        return render(request,'hr_department.html',{'department':department})


@method_decorator(login_required, name='dispatch')
class HrAddDepartmentView(View):
    def get(self,request):
        return render(request,'hr_department_add.html')
    
    def post(self,request):
        dept_name = request.POST.get("dept_name")
        Department.objects.create(department_name=dept_name)
        return redirect("/hr/department")


@method_decorator(login_required, name='dispatch')
class HrAddCategoryView(View):
    def get(self,request):
        return render(request,'hr_category_add.html')
    
    def post(self,request):
        dept_name = request.POST.get("dept_name")
        Category.objects.create(category_name=dept_name)
        return redirect("/hr/category")
    
