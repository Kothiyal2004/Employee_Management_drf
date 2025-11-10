# from django.db import models

# # Create your models here.
# from django.db import models

# class Employee(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50)
#     age = models.IntegerField()

#     class Meta:
#         db_table = 'employees'  # This matches your MySQL table name
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator, MaxValueValidator, RegexValidator, DecimalValidator
)

class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee',
        primary_key=True
    )

    # Only allows letters and spaces
    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z\s]+$',
                message="Name must contain only letters and spaces."
            )
        ]
    )

    # Age must be between 18 and 65
    age = models.IntegerField(
        validators=[
            MinValueValidator(18, message="Age must be at least 18."),
            MaxValueValidator(65, message="Age cannot be more than 65.")
        ]
    )

    # Salary must be a positive decimal number
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="Salary must be a positive value."),
            DecimalValidator(max_digits=10, decimal_places=2)
        ]
    )

    # Optional but cannot exceed 100 characters
    department = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z\s]*$',
                message="Department name can only contain letters and spaces."
            )
        ]
    )

    # Optional profile picture
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
