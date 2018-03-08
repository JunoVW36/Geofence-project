# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.conf import settings
import time
from datetime import date, timedelta, datetime
#from services.email_service import EmailService


class DataliveUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, short_name,
                    password=None, username=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            short_name=short_name,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, short_name,
                         password, username=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            short_name=short_name,
            password=password,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserPermission(models.Model):
    name = models.CharField(max_length=100) 
    is_global_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_limited_user = models.BooleanField(default=True)
    is_server_user = models.BooleanField(default=False)
    ''' this permission is used for a server client application api communication.
    A user account with this permission should be created for a server client application 
    to authenticate with the data live api .e.g. /api/auth/server/..
    '''

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name 

    def is_admin(self):
        return self.is_global_admin

    def is_customer_user(self):
        return self.is_customer

    def is_limited(self):
        return self.is_limited_user

    @staticmethod
    def get_by_name(name):
        print(name)
        return UserPermission.objects.filter(name=name).first()

    @staticmethod
    def get_limited_user():
        return UserPermission.objects.filter(is_limited_user=True, is_user=False, is_customer=False).first()


class DataliveUser(AbstractBaseUser):
    from datalive_cust_veh.models import Customer, Vehicle, VehicleTracker, VehicleGroup, Region
    from datalive_geofence.models import GeofenceGroup

    """Datalive User
    TODO:
        * Add user roles
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.EmailField( max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    telephone = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=1024, blank=True, null=True)
    # address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE)
    customers = models.ManyToManyField(Customer, related_name='user_customers', blank=True)
    regions = models.ManyToManyField(Region, related_name='user_regions', blank=True)
    vehicle_groups = models.ManyToManyField(VehicleGroup, related_name='user_vehicle_groups', blank=True)
    # geofence_groups = models.ManyToManyField(GeofenceGroup, related_name='user_geofence_groups', blank=True)
    permission = models.ForeignKey(UserPermission, blank=True, null=True)
    modules = models.ManyToManyField(
        'ModulePermission', related_name='module_users', blank=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    objects = DataliveUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'short_name']

    def __str__(self):
        return "{0} {1} {2}".format(self.first_name, self.last_name, self.email)

    def __unicode__(self):
        return "{0} {1} {2}".format(self.first_name, self.last_name, self.email)

    def fullname(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def get_customers(self):
        return self.customers.all()

    def get_customers_ids(self):
        return self.customers.all().values_list('id', flat=True)

    def update_prefs(self, prefs):
        user_prefs = UserPrefs.objects.filter(user=self).first()
        if not user_prefs:
            user_prefs = UserPrefs(user=self)
        user_prefs.time_zone = prefs.get('time_zone') if prefs.get('time_zone') else user_prefs.time_zone
        user_prefs.units_distance = prefs.get('units_distance') if prefs.get('units_distance') else user_prefs.units_distance
        user_prefs.units_volume = prefs.get('units_volume') if prefs.get('units_volume') else user_prefs.units_volume
        user_prefs.units_fuel_econ = prefs.get('units_fuel_econ') if prefs.get('units_fuel_econ') else user_prefs.units_fuel_econ
        user_prefs.save()

    def update_permission(self, permission):
            permission = UserPermission.get_by_name(permission)
            if permission:
                print('true')
                self.permission = permission
                self.save()

    @staticmethod
    def update_email_registration(user_id, email):
        user = DataliveUser.objects.filter(id=user_id).first()
        if not user:
            return None

        user.email = email
        user.save()
        return user

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @staticmethod
    def get_user_by_id(id):
        return DataliveUser.objects.filter(id=id).first()

    @staticmethod
    def get_by_email(email):
        return DataliveUser.objects.filter(email=email).first()

    @staticmethod
    def get_all():
        return DataliveUser.objects.all()\
            .select_related('permission')\
            .prefetch_related('customers', 'vehicle_groups')\
            .defer('vehicle_groups__vehicles', 'vehicle_groups__customer')

    @staticmethod
    def get_by_customer_ids(customer_ids):
        return DataliveUser.get_all().filter(customers__id__in=customer_ids)

    def update_password(self, password):
        if self.password:
            OldUserPassword.objects.create(password=self.password, user=self)
        self.set_password(password)
        self.save()


class UserPrefs(models.Model):
    """Model with all prefs related to a user.
    """
    UNITS_DISTANCE = (
        ('MLS', 'Miles'),
        ('KMS', 'Kilometers'),
    )
    UNITS_VOLUME = (
        ('GAL', 'Gallons'),
        ('LTR', 'Litres'),
    )
    UNITS_FUEL_ECON = (
        ('MPG', 'Miles per gallon'),
        ('LPK', 'Litres per 100km'),
    )
    user = models.OneToOneField(DataliveUser, on_delete=models.CASCADE, related_name='user_prefs')
    """User that these pref relate to."""
    time_zone = models.CharField(max_length=64, default='Europe/London')
    """Time zone as a string recognised by moment.js"""
    units_distance = models.CharField(max_length=3, choices=UNITS_DISTANCE, default='MLS')
    units_volume = models.CharField(max_length=3, choices=UNITS_VOLUME, default='GAL')
    units_fuel_econ = models.CharField(max_length=3, choices=UNITS_FUEL_ECON, default='MPG')

    def __str__(self):
        return "{0} {1} {2}".format(self.user, self.time_zone, self.units_distance)

    def __unicode__(self):
        return "{0} {1} {2}".format(self.user, self.time_zone, self.units_distance)

    @property
    def get_customers(self):
        return self.user.customers.all()


class UserResetPasswordToken(models.Model):
    user = models.ForeignKey(DataliveUser, related_name='user_pass_token')
    token = models.CharField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    @staticmethod
    def get_by_token(token):
        return UserResetPasswordToken.objects.filter(token=token).first()

    @staticmethod
    def create_token(user, token):
        token = UserResetPasswordToken(
            user=user, token=token, expiration_date=(timezone.now() + timedelta(days=1)))
        token.save()
        return token

    def deactivate(self):
        self.is_used = True
        self.save()

    def __unicode__(self):
        return unicode(self.user)


class OldUserPassword(models.Model):
    user = models.ForeignKey(DataliveUser, related_name='old_user_pass')
    password = models.CharField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ModulePermission(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class ModulePermissionEndpoint(models.Model):
    endpoint = models.CharField(max_length=256)
    module = models.ForeignKey(ModulePermission, related_name='endpoints')

    def __str__(self):
        return self.endpoint

    def __unicode__(self):
        return self.endpoint
