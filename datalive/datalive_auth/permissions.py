from rest_framework import permissions
from .models import DataliveUser


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class IsCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.permission.is_global_admin:
            return True

        if request.method == "POST" or request.method == "DELETE":
            return False

        if request.user.permission.is_customer:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.permission.is_global_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        for customer in request.user.customers.all():
            if customer in obj.get_customers:
                return True

        return False


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_anonymous:
            return False

        if request.user.permission.is_limited_user and request.method == "POST":
            return False
        #Prevent a User permission form POSTing
        if request.user.permission.is_user and request.method == "POST":
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.permission.is_admin():
            return True

        if request.user.permission.is_customer_user():
            for customer in request.user.customers.all():
                if customer in obj.get_customers:
                    return True

        return request.user == obj


class IsVehicle(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.permission.is_global_admin:
            return True

        if request.user.permission.is_customer:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.permission.is_global_admin:
            return True

        if obj.customer in request.user.customers.all():
            return True

        return False


class IsServer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # if request.user.is_anonymous:
        #     return False

        # if request.user.permission.is_limited_user:
        #     return False

        # if request.user.permission.is_user:
        #     return False

        # if request.user.permission.is_admin:
        #     return False
        print('********** Has_permission is_server??')
        print(request.user.permission.is_server_user)
        if request.user.permission.is_server_user and request.method == "POST":
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.permission.is_admin():
            return True

        if request.user.permission.is_customer_user():
            for customer in request.user.customers.all():
                if customer in obj.get_customers:
                    return True

        return request.user == obj


class HasModulePermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.modules.filter(
                endpoints__endpoint=request.path_info).exists():
            return True

        return False
