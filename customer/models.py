from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Course(models.Model):
    course = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.IntegerField)


class WorkApprove(models.Model):
    approve = models.CharField(max_length=50)


class HomeWork(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.CharField(max_length=200)
    status_work = models.ForeignKey(WorkApprove, on_delete=models.IntegerField)
    course = models.ForeignKey(Course, on_delete=models.IntegerField)
    customer = models.ForeignKey(Customer, on_delete=models.IntegerField)






