from django.urls import path
from account.views import *
app_name="account"

urlpatterns = [
    path("login/" , LoginAPIView.as_view() )
]

