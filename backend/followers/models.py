from django.contrib.auth import get_user_model
from django.db import models

Person = get_user_model()


class Follower(models.Model):
    user_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='following')
    following_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='followers')
# Create your models here.
