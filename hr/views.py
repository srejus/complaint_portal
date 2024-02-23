from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from accounts.models import Account
from complaints.models import Employee,Complaint

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