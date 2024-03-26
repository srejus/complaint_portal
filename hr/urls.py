from django.urls import path
from .views import *

urlpatterns = [
    path('',HrHomeView.as_view()),
    path('<int:id>',HrComplaintsView.as_view()),
    path('employees',HrEmployeesView.as_view()),
    path('complaints',HrComplaintsView.as_view()),
    path('category',HrCategoryView.as_view()),
    path('category/add',HrAddCategoryView.as_view()),
    path('department',HrDepartmentView.as_view()),
    path('department/add',HrAddDepartmentView.as_view()),
]