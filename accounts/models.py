from django.db import models
from django.contrib.auth.models import User

class hanguser(models.Model):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    code = models.CharField(max_length=25, unique=True)

class resetpasscode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=25, unique=True)


class changemail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    newemail = models.EmailField()
    code = models.CharField(max_length=25, unique=True)