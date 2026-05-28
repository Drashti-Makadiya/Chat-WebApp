from django.contrib import admin
from apps.accounts.models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'email', 'profile_image','role', 'is_active', 'is_staff', 'is_online', 'phone_number')
    search_fields = ('user_name', 'email')
    list_filter = ('is_active', 'is_staff', 'role')
    
    