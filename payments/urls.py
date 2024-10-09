from django.urls import path
from . import views

urlpatterns = [
    path('initiate/<int:course_id>/', views.initiate_payment, name='initiate_payment'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('failure/', views.payment_failure, name='payment_failure'),
    path('history/', views.payment_history, name='payment_history'),
]
