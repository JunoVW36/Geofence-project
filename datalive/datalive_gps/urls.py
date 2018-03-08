from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework import routers
#from .views import TrackerPointViewSet
#from .views import CustomGet

router = routers.DefaultRouter()
router.register(r'trace', views.TrackerPointViewSet, base_name='trace')
router.register(r'vehicle/timesheet', views.TimeSheetViewSet, base_name='timesheet')
router.register(r'vehicle/trip', views.TripViewSet, base_name='trip')
router.register(r'track', views.TrackViewSet, base_name='track')
#router.register(r'vehicle/message', views.VehicleMessageViewSet, base_name='vehicle_message')
#router.register(r'track_get', CustomGet, base_name='track_get')

urlpatterns = [
    url(r'vehicle/message', views.VehicleMessageView.as_view(), name="vehicle_message"),
]
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls

#urlpatterns = [
#    url(r'^track_get/', views.CustomGet.as_view(), name="track_get"),
#]
#urlpatterns = format_suffix_patterns(urlpatterns)
#urlpatterns += router.urls
