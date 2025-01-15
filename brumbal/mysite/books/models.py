import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import random  # Ensure random is imported if you're using random.choice
from django.contrib.auth.models import AbstractUser

class Book(models.Model):
    author = models.CharField(max_length=200, default="Unknown")
    title = models.CharField(max_length=200)  
    pub_date = models.DateTimeField("Publikované")
    image = models.ImageField(upload_to='books/')
    def __str__(self):
        return self.title
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now



class Review(models.Model):
    def __str__(self):
        return self.review_text
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  
    review_text = models.CharField(max_length=200)  
    rating = models.IntegerField(default=0)  
