from django.urls import path
from manager.views import *
app_name="manager"

urlpatterns = [
    path('manager-home/' ,              ManagerHomeAPIView.as_view()),
    
    # Project
    path('add-project/',           AddProjectAPIView.as_view(), name='add-project'),
    path('view-project/<int:pk>/', AddProjectAPIView.as_view(), name='view-project'),
    path('edit-project/<int:pk>/', AddProjectAPIView.as_view(), name='edit-project'),
    path('update-project/<int:pk>/', AddProjectAPIView.as_view(), name='update-project'),

    # Team

    path('add-team/',           add_team),

    ## TASK 
    path('assign-task/' , assign_task),
    

]

