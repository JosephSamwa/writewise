from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


class TimestampIDField(models.BigAutoField):
    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, (int, str)):
            return super().get_prep_value(value)
        if isinstance(value, timezone.datetime):
            return int(value.timestamp())
        return super().get_prep_value(value)
class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    students_enrolled = models.DecimalField(max_digits=100, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    id = TimestampIDField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new enrollment
            if Enrollment.objects.filter(user=self.user, course=self.course).exists():
                raise ValidationError("You are already enrolled in this course.")
        super().save(*args, **kwargs)
