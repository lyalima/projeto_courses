from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserEmailVerificationCode


class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["id", "username", "is_superuser", "email", "full_name", "email_verified",]


class UserEmailVerificationCodeAdmin(admin.ModelAdmin):

    model = UserEmailVerificationCode
    list_display = ["id", "user", "code",]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserEmailVerificationCode, UserEmailVerificationCodeAdmin)
