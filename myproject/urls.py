from django.contrib import admin
from django.urls import path, include
from users.views import about, contact, activation_invalid, home, register, login_view, logout_view, dashboard
from courses.views import course_list, user_course_details, course_detail, enroll
from payments.views import initiate_payment, payment_success, payment_failure as payments_payment_failure, payment_history

urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about/', about, name='about'),
    path('activation_invalid/', activation_invalid, name='activation_invalid'),
    path('contact/', contact, name='contact'),
   # path('users/', include('django.contrib.auth.urls')),  # Include built-in auth URLs
    path('enroll/<int:course_id>/', enroll, name='enroll'),
    path('', home, name='home'),
    path('payment_failure/', payments_payment_failure, name='payment_failure'),
    path('payments/success/<int:payment_id>/', payment_success, name='payment_success'),
    path('admin/', admin.site.urls),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('payments/', include('payments.urls')),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),  # Ensure this line exists
    path('dashboard/', user_course_details, name='dashboard'),
    path('signup/', register, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('payment_success/', payment_success, name='payment_success'),
    path('user_course_details/', user_course_details, name='user_course_details'),
    path('payments/history/', payment_history, name='payment_history'),
    path('payments/initiate/<int:course_id>/', initiate_payment, name='initiate_payment'),
]
