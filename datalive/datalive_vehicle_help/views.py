from rest_framework import viewsets, permissions, generics, views, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from .models import *
from .serializers import *
from datalive_cust_veh.serializers import *
from datalive_auth.permissions import IsCustomer, IsUser, IsVehicle
# Create your views here.



class CustomerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class VehicleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class VehiclesVehicleGroupsView(generics.ListCreateAPIView):
    serializer_class = VehicleGroupForVehicleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        vehicle_id = self.kwargs['pk']
        return VehicleGroup.get_by_vehicle_id(vehicle_id)