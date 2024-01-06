from django.contrib import admin
from .models import User,Notification
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=[
        "email",
        "username",
        "mobile",
        "otp",
        "active"
    ]
admin.site.register(Notification)    