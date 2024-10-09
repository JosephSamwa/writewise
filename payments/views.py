from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Payment, PurchasedItem
from courses.models import Course, Enrollment
from .forms import PaymentForm  # Import the PaymentForm
from .payment_utils import process_payment  # Assuming you have a custom payment processing function

import logging
logger = logging.getLogger(__name__)

@login_required
def initiate_payment(request, course_id):
    logger.debug(f"Received course_id: {course_id}")
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.course = course
            payment.save()
            return redirect('payment_success', payment_id=payment.id)
    else:
        form = PaymentForm()
    return render(request, 'payments/initiate_payment.html', {'course': course, 'form': form})

@login_required
def payment_success(request, payment_id):
    try:
        payment = get_object_or_404(Payment, id=payment_id)
        return render(request, 'courses/payment_success.html', {'payment': payment})
    except Payment.DoesNotExist:
        # Add logging or print statements here for debugging
        print(f"Payment with id {payment_id} does not exist.")
        return render(request, 'courses/payment_failure.html', {'error': 'Payment not found'})

@login_required
def payment_failure(request):
    return render(request, 'courses/payment_failure.html', {'error': 'Payment failed. Please try again.'})

@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'payments/payment_history.html', {'payments': payments})
