from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.utils import timezone

from complaints.models import Complaint
from accounts.models import Account


# Create your views here.
@method_decorator(login_required, name='dispatch')
class EmployeeHomeView(View):
    def get(self,request,id=None):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'GOV_EMPLOYEE':
            return redirect("/")
        
        complaints = Complaint.objects.filter(employee_id__user__user=request.user)
        if id:
            complaints = Complaint.objects.filter(employee_id__user__user=request.user,id=id).first()
            return render(request,'view_compliant.html',{'complaint':complaints})
        
        return render(request,'employee_complaints.html',{'complaints':complaints})
    

    def post(self,request,id=None):
        reply = request.POST.get("reply")
        compliant = Complaint.objects.get(id=id)
        compliant.employee_response = reply
        compliant.status = 'PROCESSING'
        compliant.employee_response_added_at = timezone.now()
        compliant.save()
        return redirect("/employee/")