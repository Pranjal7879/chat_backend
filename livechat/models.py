from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class User(AbstractUser):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'name']  

    def __str__(self):
        return self.email



