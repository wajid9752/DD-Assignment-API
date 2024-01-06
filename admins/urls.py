from django.urls import path
from admins.views import *
app_name="admins"

urlpatterns = [
    path('admin-home/' , AdminHomeAPIView.as_view()),
    path('add-employee/' , AddEmployeeAPIView.as_view()),
    path('update-user-status/<int:pk>/' , update_user_status),
    path('filter-user/' , filter_user),
]

