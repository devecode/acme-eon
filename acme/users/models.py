from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    saldo_inicial = models.FloatField(default=1000)
    saldo_final = models.FloatField(default=0)

    def __str__(self):
        return str(self.username)
