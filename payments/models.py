from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime
import uuid

class TimestampIDField(models.BigAutoField):
    def get_prep_value(self, value):
        if isinstance(value, (int, str)):
            return super().get_prep_value(value)
        if isinstance(value, timezone.datetime):
            return int(value.timestamp())
        return super().get_prep_value(value)

class BasePayment(models.Model):
    currency = models.CharField(max_length=10, default='USD')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='base_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ], default='pending')

    class Meta:
        abstract = True

    def __str__(self):
        return f"Payment of ${self.amount} by {self.user.username}"

    def get_timestamp_as_int(self):
        return int(self.timestamp.timestamp())

class PurchasedItem(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchased_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.user})"

    class Meta:
        app_label = 'payments'

class Payment(BasePayment):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    items = models.ManyToManyField('courses.Enrollment')  # Corrected ManyToManyField declaration
    transaction_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    phone_number = models.CharField(max_length=15, default='000-000-0000')
    is_used = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return f"Payment of ${self.amount} for {self.course.title} by {self.user.username}"

    def get_failure_url(self):
        return 'payment_failure_url'

    def get_success_url(self):
        return 'payment_success_url'

    def get_purchased_items(self):
        yield PurchasedItem(
            name='Course Payment',
            sku='12345',
            quantity=1,
            price=self.amount,
            currency='USD',
        )

    def get_timestamp_as_int(self):
        return int(self.timestamp.timestamp())

    class Meta:
        app_label = 'payments'
