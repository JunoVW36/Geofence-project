# urls for geofence page

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^geofence_groups/$', views.GeofenceGroupsView.as_view(), name="geofence-groups"),
    url(r'^geofence_categories/$', views.GeofenceCategoryView.as_view(), name="geofence-gategories"),
    url(r'^geofence/', views.GeofencesView.as_view(), name="geofence-view")
]

urlpatterns = format_suffix_patterns(urlpatterns)
