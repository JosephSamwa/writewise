from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from courses.models import Course

class CustomUser(AbstractUser):  # Corrected the class name to CustomUser
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    time_spent = models.IntegerField()
    fee_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Not Initiated')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_payment_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username

"""class MpesaTransaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    transaction_date = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transaction_id} - {self.amount}"
"""