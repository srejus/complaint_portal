from django.urls import path
from .views import *

urlpatterns = [
    path('register',RegisterComplaintView.as_view()),
    path('',ComplaintView.as_view()),
    path('<int:id>',ComplaintView.as_view()),
    path('delete/<int:id>',DeleteComplaintView.as_view()),
    path('view/<int:id>',ViewComplaintView.as_view()),
]