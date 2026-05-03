from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None  # remove username

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)

    SECURITY_QUESTIONS = [
        ('school', 'School Name'),
        ('player', 'Favorite Player'),
        ('nickname', 'Nickname'),
    ]

    security_question = models.CharField(max_length=20, choices=SECURITY_QUESTIONS)
    security_answer = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email