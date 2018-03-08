from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
# from datalive_cust_veh.views import VehicleView, CustomerView


urlpatterns = [
    # url(r'^vehicles_group_contact_list/', views.VehicleGroupContactListView.as_view(), name="vehicles-user-list"),
     url(r'^help/vehicle/(?P<pk>[0-9]+)/$', views.VehicleView.as_view(), name="help-vehicle-detail"),
     url(r'^help/customer/(?P<pk>[0-9]+)/$', views.CustomerView.as_view(), name="help-customers-detail"),
     url(r'^help/vehicle/(?P<pk>[0-9]+)/vehicle_groups', views.VehiclesVehicleGroupsView.as_view(), name="vehicles-vehicle-groups"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
