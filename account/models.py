from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin



def validate_allowed_domains(value):
    # List of disallowed domains
    allowed_domains = [
    'drone.com',
    'drone.in',
    'drone.co',
    'drone.org',
    'drone.tech',
    ]

    email_domain = value.split('@')[-1]
    if not email_domain.lower() in allowed_domains:
        raise ValidationError("Emails from {} domain are not allowed.".format(email_domain))


    

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_active=True, is_admin=False):
        if not email:
            raise ValueError('users must have a email')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            email=email
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.role = "admin"
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,


        )
        return user

class User(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    username        = models.CharField(max_length=100 , null=True , blank=True)
    email           = models.CharField(max_length=100 , unique=True , validators=[validate_allowed_domains])
    mobile          = models.CharField("Mobile Number", max_length=15)
    otp             = models.IntegerField(blank=True, null=True)
    role            = models.CharField(max_length=20, choices=ROLE_CHOICES)
    active          = models.BooleanField(default=True)
    staff           = models.BooleanField(default=False)
    admin           = models.BooleanField(default=False) 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    objects = UserManager()



    # access_token 
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
    class Meta:
        ordering = ['-created_at']


class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Notification(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    
    class Meta:
        ordering = ['-created_at']







