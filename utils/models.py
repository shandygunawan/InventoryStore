from django.db import models

class GlobalConfig(models.Model):
    key = models.TextField()
    value = models.TextField()