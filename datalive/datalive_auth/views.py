from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, views, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings
from .models import DataliveUser, OldUserPassword, UserResetPasswordToken, \
    UserPermission
from .serializers import *
from datalive_cust_veh.models import Customer, Vehicle, VehicleTracker, VehicleGroup 
from datalive_auth.permissions import IsCustomer, IsUser
from datetime import datetime
from django.utils import timezone
from utilities.helpers import Helpers


class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataliveUser.objects.all()
    serializer_class = DataliveUserSerializer
    permission_classes = (IsUser, )
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.update_prefs(request.data)
        customers = request.data.get('customers', [])
        vehicle_groups = request.data.get('vehicle_groups', [])
        modules = request.data.get('modules', [])
        email = request.data.get('email')
        permission = request.data.get('permission', '')
        user.update_permission(permission)
        exist_user = DataliveUser.get_by_email(email)
        if not email or exist_user and exist_user != user:
            raise serializers.ValidationError("Email already exist")

        user.customers.clear()
        if customers:
            customer_ids = [customer['id'] for customer in customers]
            customers = Customer.objects.filter(id__in=customer_ids)
            for customer in customers:
                user.customers.add(customer) if customer else None

        user.vehicle_groups.clear()
        vehicle_groups = [group['id'] for group in vehicle_groups]
        groups_list = VehicleGroup.objects.filter(id__in=vehicle_groups)
        user.vehicle_groups.add(*groups_list)
        if modules:
            user.modules.clear()
            modules = [mod['id'] for mod in modules]
            module_list = ModulePermission.objects.filter(id__in=modules)
            user.modules.add(*module_list)

        return super(UserView, self).update(request, *args, **kwargs)


class UserListView(generics.ListCreateAPIView):
    queryset = DataliveUser.objects.all()
    serializer_class = DataliveUserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsUser, )

    def create(self, request, *args, **kwargs):
        print('USER self')
        print(self)
        email = request.data.get('email')
        exist_user = DataliveUser.get_by_email(email)
        if not email or exist_user:
            return Response({'message': 'Email already exist'}, status=status.HTTP_400_BAD_REQUEST)
            raise serializers.ValidationError("Email already exist")
        return super(UserListView, self).create(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        if self.request.user.permission.is_global_admin:
            return DataliveUser.get_all()
        customer_ids = self.request.user.customers.all().values_list('id', flat=True)
        return DataliveUser.get_by_customer_ids(customer_ids)


class UserGroupListView(generics.ListAPIView):
    queryset = DataliveUser.objects.all()
    serializer_class = DataliveUserSmallSerializer
    permission_classes = (IsUser, )

    def get_queryset(self):
        if self.request.user.permission.is_user or self.request.user.is_anonymous:
            return []
        if self.request.user.permission.is_global_admin:
            return DataliveUser.get_all()
        customer_ids = self.request.user.customers.all().values_list('id', flat=True)
        return DataliveUser.get_by_customer_ids(customer_ids)


class UserDeleteView(generics.CreateAPIView):
    queryset = DataliveUser.objects.all()
    serializer_class = DataliveUserSerializer
    permission_classes = (IsUser, )

    def post(self, request, *args, **kwargs):
        DataliveUser.objects.filter(id__in=request.data).delete()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)


class CurrentUserView(generics.RetrieveAPIView):
    queryset = DataliveUser.get_all()
    serializer_class = DataliveUserSerializer

    def get_object(self):
        obj = self.request.user
        return obj


class UserPermissionsView(generics.ListAPIView):
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = (IsCustomer, )



class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = DataliveUser
    permission_classes = (IsUser, )

    def get_object(self, queryset=None):
        return DataliveUser.get_user_by_id(int(self.kwargs.get('pk')))

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            OldUserPassword.objects.create(password=serializer.data.get("old_password"), user=self.object)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):

    def post(self, request, *args, **kwargs):
        user = DataliveUser.get_by_email(request.data.get("email"))
        if not user:
            return Response({"message": "Wrong email address. Please try again"}, status=status.HTTP_400_BAD_REQUEST)
        token = Helpers.unique_reset_token_key(user)
        UserResetPasswordToken.create_token(user, token)
        return Response({"message": "%s, %s" % (token,user)})
        EmailService().send_reset_password_email(user=user, token=token)
        print(request.data)
        return Response({"message": "Reset token has successfully been created."}, status=status.HTTP_200_OK)


class ResetPassswordTokenView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = DataliveUser

    def get_object(self, queryset=None):
        return DataliveUser.get_user_by_id(int(self.kwargs.get('pk')))

    def update(self, request, *args, **kwargs):
        request_token = request.data.get('token')
        token = UserResetPasswordToken.get_by_token(request_token)
       
        if not token:
            return Response({"token": "No Token", "status": "No token", "message": "No token found for this user"}, status=status.HTTP_400_BAD_REQUEST)
        elif token.is_used:
            return Response({"token": "Token used", "status": "token used", "message": "This password token has been used already"}, status=status.HTTP_400_BAD_REQUEST)
        elif token.expiration_date < timezone.now():
            return Response({"token": "Token expired", "status": "token expired", "message": "This password token has expired. Reset password again"}, status=status.HTTP_400_BAD_REQUEST)

        token.user.update_password(request.data.get("password"))
        token.deactivate()
        return Response({"message": "Password changed successfully.", "status": "success"}, status=status.HTTP_200_OK)


class SetPassswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = DataliveUser

    def get_object(self, queryset=None):
        return DataliveUser.get_user_by_id(int(self.kwargs.get('pk')))

    def update(self, request, *args, **kwargs):
        request_token = request.data.get('token')
        token = UserResetPasswordToken.get_by_token(request_token)
        if not token:
            return Response({"token": "No Token", "status": "No token", "message": "No token found for this user"}, status=status.HTTP_400_BAD_REQUEST)
        elif token.is_used:
            return Response({"token": "Token used", "status": "token used", "message": "This password token has been used already"}, status=status.HTTP_400_BAD_REQUEST)
        elif token.expiration_date < timezone.now():
            return Response({"token": "Token expired", "status": "token expired", "message": "This password token has expired. Reset password again"}, status=status.HTTP_400_BAD_REQUEST)

        token.user.update_password(request.data.get("password"))
        token.deactivate()
        return Response({"message": "Password changed successfully.", "status": "success"}, status=status.HTTP_200_OK)


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username/email and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = DataliveJSONWebTokenSerializer


class ModulePermissionsView(generics.ListAPIView):
    queryset = ModulePermission.objects.all()
    serializer_class = ModulePermissionSerializer
    permission_classes = (IsCustomer, )

