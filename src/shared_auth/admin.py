from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from src.shared_auth.models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

    verbose_name_plural = 'UserProfiles'


class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)

