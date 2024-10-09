from django.urls import path, include
from users.views import home, register, login_view, logout_view, dashboard
from courses.views import course_list, user_course_details, course_detail, enroll
from payments.views import initiate_payment, payment_success, payment_failure as payments_payment_failure, payment_history
from django.contrib.auth import views as auth_views

app_name = 'courses'

urlpatterns = [
    path('enroll/<int:course_id>/', enroll, name='enroll'),
    path('', home, name='home'),
    path('payment_failure/', payments_payment_failure, name='payment_failure'),
    path('payments/success/<int:payment_id>/', payment_success, name='payment_success'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('payments/', include('payments.urls')),
    path('list/', course_list, name='course_list'),  # Ensure this line exists
    path('course/<int:course_id>/', course_detail, name='course_detail'),  # Added course_id parameter
    path('course/<int:course_id>/enroll/', enroll, name='enroll'),  # Added course_id parameter
    path('dashboard/', user_course_details, name='dashboard'),
    path('signup/', register, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('payment_success/', payment_success, name='payment_success'),
    path('user_course_details/', user_course_details, name='user_course_details'),
    path('payments/history/', payment_history, name='payment_history'),
    path('payments/initiate/<int:course_id>/', initiate_payment, name='initiate_payment'),
]
