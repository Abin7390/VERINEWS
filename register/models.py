from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.timezone import now

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default='example@123.com')    
    password = models.CharField(max_length=128)  # Store hashed password
    age = models.CharField(max_length=128, default='20')  
    last_login = models.DateTimeField(default=now, blank=True)
    is_superUser = models.CharField(max_length=100, default="user", blank=True)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)