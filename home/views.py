from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import Account


# Create your views here.

# @method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self,request):
        if request.user.is_authenticated:
            acc = Account.objects.get(user=request.user)
            if acc.user_type == 'GOV_EMPLOYEE':
                return redirect("/employee")
            if acc.user_type == 'ADMIN':
                return redirect("/hr")
            if acc.user_type == 'USER':
                return render(request,'index.html')
            
        return render(request,'index_no_login.html')