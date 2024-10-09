from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser
from courses.models import Course, Enrollment  # Import models from courses app
from payments.models import Paymenttt  # Import models from payments app

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active', 'date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username',)
    ordering = ('date_joined',)
    readonly_fields = ('date_joined', 'last_login')  # Added readonly fields

admin.site.register(CustomUser, CustomUserAdmin)

class EnrollmentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            obj.save()
            self.message_user(request, f'The enrollment “{obj.user} enrolled in {obj.course}” was added successfully.', level=messages.SUCCESS)
        except ValidationError as e:
            self.message_user(request, e.message, level=messages.ERROR)
admin.site.register(Enrollment, EnrollmentAdmin)

#other models
admin.site.register(Course)
admin.site.register(Paymenttt)

#custom headers
admin.site.site_header = "WriteWise Admin Panel"
admin.site.site_title = "WriteWise Admin Panel"
admin.site.index_title = "WrteWise Admin Panel"

