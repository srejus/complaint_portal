from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ComplaintView(View):
    def get(self,request,id=None):
        complaints = Complaint.objects.filter(user__user=request.user)
        if id:
            complaints = Complaint.objects.filter(user__user=request.user,id=id).first()
            return render(request,'view_compliant.html',{'complaint':complaints})
        
        return render(request,'user_complaints.html',{'complaints':complaints})



@method_decorator(login_required, name='dispatch')
class RegisterComplaintView(View):
    def get(self,request):
        employees = Employee.objects.all()
        return render(request,'register_complaint.html',{'employees':employees})

    def post(self,request):
        complaint_title = request.POST.get("complaint_title")
        complaint_desc = request.POST.get("complaint_desc")
        eid = request.POST.get("eid")
        proof = request.FILES.get("proof")

        acc = Account.objects.get(user=request.user)
        employee = Employee.objects.get(id=eid)

        Complaint.objects.create(user=acc,employee_id=employee,
                                 proof=proof,complaint_title=complaint_title,
                                 complaint_desc=complaint_desc)
        
        return redirect("/")
    

@method_decorator(login_required, name='dispatch')
class DeleteComplaintView(View):
    def get(self,request,id):
        Complaint.objects.filter(id=id).delete()
        return redirect("/complaints")