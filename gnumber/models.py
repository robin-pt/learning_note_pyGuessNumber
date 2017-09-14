from django.db import models
from django.contrib.auth.models import User

class Results(models.Model):
    """ user's result """
    user = models.OneToOneField(User, unique=True, related_name='result')
    result = models.IntegerField(default=0)
    def __str__(self):
        return self.user
