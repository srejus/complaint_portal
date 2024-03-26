from django.db import models
from accounts.models import Account

# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.department_name)
    

class Category(models.Model):
    category_name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.category_name)
    
    

class Employee(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='employee')
    department = models.ForeignKey(Department,on_delete=models.CASCADE,related_name='employee_department',null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='employee_category',blank=True,null=True)


class Complaint(models.Model):
    STATUS_CHOICES = (
        ('CREATED','CREATED'),
        ('PROCESSING','PROCESSING'),
        ('CLOSED','CLOSED'),
    )
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='complaint_user')
    employee_id = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='complaint_employee')
    proof = models.FileField(null=True,blank=True)
    complaint_title = models.CharField(max_length=100)
    complaint_desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,default='CREATED')
    employee_response = models.TextField(null=True,blank=True)
    employee_response_added_at = models.DateTimeField(null=True,blank=True)
    hr_response = models.TextField(null=True,blank=True)
    hr_response_added_at = models.DateTimeField(null=True,blank=True)
