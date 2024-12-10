from django.db import models

# Create your models here.
class User(models.Model):
    ID_User = models.AutoField(primary_key=True)
    Username =models.CharField(max_length=100, unique=True)
    Email = models.EmailField(max_length=100, unique=True)
    Password = models.CharField(max_length=100)
    User_created=models.DateTimeField(auto_now_add=True)
    
