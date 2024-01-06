from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("account.urls",namespace="account")),
    path('api/', include("employee.urls",namespace="employee")),
    path('api/', include("admins.urls",namespace="admins")),
    path('api/', include("manager.urls",namespace="manager")),
]
