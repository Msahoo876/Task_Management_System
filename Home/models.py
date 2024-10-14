# models.py
from django.db import models

class Crud(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    status = models.CharField(max_length=20, choices=[('todo', 'To Do'), ('inprogress', 'In Progress'), ('done', 'Done')])

class User(models.Model):
    Fast_name = models.CharField(max_length=100)
    Last_name = models.CharField(max_length=100)
    Email_Id = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Field_in_list = models.CharField(max_length=1000, default='black')

class Assign(models.Model):
    Task_Title = models.CharField(max_length=100)
    Assigned_User = models.CharField(max_length=100)
    Created_User = models.CharField(max_length=100)

class Feedback(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Message = models.TextField(max_length=100)
