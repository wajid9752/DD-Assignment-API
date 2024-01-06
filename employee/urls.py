from django.urls import path
from employee.views import *
app_name="employee"

urlpatterns = [
    path('employee-home/' ,  EmployeeHomeAPIView.as_view()),
    path('update-task-status/<int:pk>/' ,  update_task_status),
    path('filter-task/' ,  filter_task),
]

