from django.urls import path
from .views import *

urlpatterns = [
    path('',EmployeeHomeView.as_view()),
    path('<int:id>',EmployeeHomeView.as_view()),
]