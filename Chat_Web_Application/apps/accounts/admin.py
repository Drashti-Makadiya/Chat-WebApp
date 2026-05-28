from django.contrib import admin
from apps.accounts.models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active', 'is_staff', 'is_online', 'phone_number')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'role')