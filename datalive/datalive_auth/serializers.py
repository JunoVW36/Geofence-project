from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField, ListField
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework_jwt.serializers import jwt_payload_handler,\
    jwt_encode_handler
from rest_framework_jwt.compat import get_username_field, PasswordField
from .models import DataliveUser, UserPrefs, UserPermission, \
    UserResetPasswordToken, ModulePermission
from datalive_cust_veh.serializers import *
from datalive_cust_veh.models import VehicleGroup, VehicleTracker, Vehicle, Customer
from services.email_service import EmailService
from utilities.helpers import Helpers

class UserPrefsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPrefs
        fields = '__all__'


class UserPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPermission
        fields = '__all__'


class ModulePermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModulePermission
        fields = ('id', 'name',)


class DataliveUserSmallSerializer(serializers.ModelSerializer):
    edit_status_field = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = DataliveUser
        fields = ('id', 'email', 'first_name', 'last_name', 'short_name', 'is_active', 'edit_status_field')

    def get_edit_status_field(self, obj):
        request = self.context.get("request")
        if request and request.user.permission.is_customer:
            user_customers = self.context.get('request').user.customers.all().values_list('id', flat=True)
            obj_customers = obj.get_customers_ids()
            if set(user_customers) & set(obj_customers):
                return True
        if request and request.user.permission.is_global_admin:
            return True
        return False


class LoggedInUserSerializer(serializers.ModelSerializer):
    permission = UserPermissionSerializer(required=False, read_only=True)
    prefs = SerializerMethodField(required=False)
    modules = ModulePermissionSerializer(required=False, many=True, read_only=True)

    def get_prefs(self, instance):
        prefs = UserPrefs.objects.filter(user=instance).first()
        serializer = UserPrefsSerializer(instance=prefs, required=False)
        return serializer.data

    class Meta:
        model = DataliveUser
        fields = ('id', 'email', 'first_name', 'last_name', 'short_name', 'permission', 'modules', 'prefs')


class DataliveUserSerializer(DataliveUserSmallSerializer):

    vehicle_groups = SerializerMethodField(required=False)
    customers = SerializerMethodField(required=False, read_only=True)
    prefs = SerializerMethodField(required=False)
    permission = UserPermissionSerializer(required=False, read_only=True)
    email = serializers.EmailField(required=True)
    modules = ModulePermissionSerializer(
        required=False, many=True, read_only=True)

    def get_vehicle_groups(self, instance):
        groups = instance.vehicle_groups.defer('vehicles', 'customer', 'user_vehicle_groups')
        serializer = VehicleGroupUserSerializer(instance=groups, many=True, required=False)
        return serializer.data

    def get_customers(self, instance):
        serializer = CustomerSerializerMinimal(instance=instance.customers, many=True, required=False)
        # serializer = CustomerSerializer(instance=instance.customers, many=True, required=False)
        return serializer.data

    def get_prefs(self, instance):
        prefs = UserPrefs.objects.filter(user=instance).first()
        serializer = UserPrefsSerializer(instance=prefs, required=False)
        return serializer.data

    def create(self, validated_data):
        customers = [customer['id'] for customer in self.initial_data.pop('customers')]
        groups = [group['id'] for group in self.initial_data.pop('vehicle_groups')]
        modules = [mod['id'] for mod in self.initial_data.pop('modules', [])]

        permission_name = self.initial_data.pop('permission')
        self.initial_data['permission'] = UserPermission.get_by_name(permission_name) if permission_name else UserPermission.get_limited_user()

        user = DataliveUser.objects.create(**self.initial_data)

        customers_list = Customer.objects.filter(id__in=customers)
        user.customers.add(*customers_list)

        groups_list = VehicleGroup.objects.filter(id__in=groups)
        user.vehicle_groups.add(*groups_list)

        module_list = ModulePermission.objects.filter(id__in=modules)
        user.modules.add(*module_list)

        token = Helpers.unique_reset_token_key(user)
        UserResetPasswordToken.create_token(user, token)
        EmailService().send_welcome_password_email(user=user, token=token)
        return user


    class Meta:
        model = DataliveUser
        fields = ('id', 'email', 'first_name', 'last_name', 'short_name', 'is_active', 'is_admin',
                  'customers', 'vehicle_groups', 'prefs', 'telephone', 'address', 'permission',
                  'created_date', 'edit_status_field', 'modules')
        read_only_fields = ('email', 'is_active', 'is_admin', 'permission', 'edit_status_field')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataliveUser
        fields = ('email', 'short_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            short_name=validated_data['short_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user




class DataliveJSONWebTokenSerializer(serializers.Serializer):
    """
    Serializer class used to validate a username/email and password of a user.

    Returns a JSON Web Token that can be used to authenticate later calls.
    """

    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    password = PasswordField(required=True)

    @property
    def object(self):
        return self.validated_data

    def validate(self, attrs):

        # Raise error if both username and email are missing
        if not attrs.get('username') and not attrs.get('email'):
            msg = _('Must include either "username" or "email".')
            raise serializers.ValidationError(msg)

        credentials = {
            'username': attrs.get('username'),
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }
        # Authenticate the user and return the token if successful
        user = authenticate(**credentials)
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg)

            payload = jwt_payload_handler(user)

            return {
                'token': jwt_encode_handler(payload),
                'user': user
            }
        else:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg)


def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.

    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    # get more user fields using a serializer
    user_full = DataliveUser.objects.filter(email=user.email).first()
    user_serializer = LoggedInUserSerializer(instance=user_full)

    return {
        'token': token,
        'user': user_serializer.data
    }
