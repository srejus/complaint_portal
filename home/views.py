from django.shortcuts import render,redirect
from django.views import View

from accounts.models import Account


# Create your views here.
class IndexView(View):
    def get(self,request):
        if request.user.is_authenticated:
            acc = Account.objects.get(user=request.user)
            if acc.user_type == 'GOV_EMPLOYEE':
                return redirect("/employee")
            if acc.user_type == 'HR':
                return redirect("/hr")
            
        return render(request,'index.html')