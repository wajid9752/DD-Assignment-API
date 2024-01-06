from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.db.models import Count

from account.models import *
from manager.models import *

from account.serializers import *
from admins.serializers import *
from employee.serializers import *
from manager.serializers import *



