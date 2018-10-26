from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    displayed_name = models.CharField(max_length=26)
    description = models.TextField(max_length=280)
    photo_url = models.URLField(default='https://gladstoneentertainment.com/wp-content/uploads/2018/05/avatar-placeholder.gif')
    redirect_url = models.URLField(default='www.google.com')