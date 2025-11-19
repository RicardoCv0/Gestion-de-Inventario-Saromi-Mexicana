from django.db import models
from django.contrib.auth.models import User

ROLES = [
    ('gerente', 'Gerente'),
    ('supervisor', 'Supervisor'),
    ('surtidor', 'Surtidor de material'),
    ('asistente', 'Asistente de producción'),
    ('contador', 'Contador'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"