from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	url(r'^customers/get_current_customer/$', views.CurrentCustomerView.as_view(), name="customers-current-list"),
    url(r'^customers/', views.CustomerListView.as_view(), name="customers-list"),
    url(r'^customers_minimal/', views.CustomerMinimalListView.as_view(), name="customer-minimal-list"),
    url(r'^customers_delete/', views.CustomerDeleteView.as_view(), name="customers-delete"),
    url(r'^customer/(?P<pk>[0-9]+)/$', views.CustomerView.as_view(), name="customers-detail"),
    url(r'^vehicles/', views.VehicleListView.as_view(), name="vehicles-list"),
    url(r'^vehicles_group_list/', views.VehicleUserListView.as_view(), name="vehicles-user-list"),
    url(r'^vehicles_delete/', views.VehicleDeleteView.as_view(), name="vehicles-delete"),
    url(r'^vehicle/(?P<pk>[0-9]+)/$', views.VehicleView.as_view(), name="vehicles-detail"),
    url(r'^vehicle/(?P<pk>[0-9]+)/vehicle_groups', views.VehiclesVehicleGroupsView.as_view(), name="vehicles-vehicle-groups"),
    url(r'^vehicle_man_models/', views.VehicleManModelsListView.as_view(), name="vehicle-man-model-list"),
    url(r'^vehicle_manufacturers/', views.VehicleManufacturersListView.as_view(), name="vehicle-manufacturer-list"),
    url(r'^vehicles_groups/', views.VehicleGroupListView.as_view(), name="vehicles-groups-list"),
    url(r'^vehicles_groups_for_user_list/', views.VehicleGroupUserListView.as_view(), name="vehicles-groups-user-list"),
    url(r'^vehicles_groups_delete/', views.VehicleGroupDeleteView.as_view(), name="vehicles-groups-delete"),
    url(r'^vehicles_group/(?P<pk>[0-9]+)/$', views.VehicleGroupView.as_view(), name="vehicles-group-detail"),
    url(r'^vehicles_trackers/', views.VehicleTrackerListView.as_view(), name="vehicles-trackers-list"),
    url(r'^vehicles_tracker/(?P<pk>[0-9]+)/$', views.VehicleTrackerView.as_view(), name="vehicles-tracker-detail"),
    url(r'^regions/$', views.RegionListView.as_view(), name="regions-list"),
    url(r'^region_depots_stats/(?P<region_id>[0-9]+)/$', views.RegionDepotsStatsView.as_view(), name="region-depots-stats"),
    url(r'^region_stats/(?P<pk>[0-9]+)/$', views.RegionStatsView.as_view(), name="region-stats"),
    url(r'^depot_stats/(?P<pk>[0-9]+)/$', views.DepotStatsView.as_view(), name="depot-stats"),
    url(r'^upload_vehicles/$', views.UploadVehiclesView.as_view(), name="upload-vehicles")
]

urlpatterns = format_suffix_patterns(urlpatterns)
