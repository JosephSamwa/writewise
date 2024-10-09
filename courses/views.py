from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from users.models import CustomUser
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
import logging
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

logger = logging.getLogger(__name__)

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course, 'course_id': course_id})

@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return render(request, 'courses/enroll.html', {'course': course, 'error': 'You are already enrolled in this course.'})
        
        # Create the enrollment
        Enrollment.objects.create(user=request.user, course=course)
        return redirect('courses:course_detail', course_id=course.id)
    
    return render(request, 'courses/enroll.html', {'course': course})

def home(request):
    return render(request, 'courses/home.html')


@login_required
def user_course_details(request):
    if not request.user.is_authenticated:
        return redirect('users/login.html')
    user = request.user
    enrollments = Enrollment.objects.filter(user=user).select_related('course')
    print(enrollments)
    return render(request, 'users/dashboard.html', {'user': user, 'enrollments': enrollments})
