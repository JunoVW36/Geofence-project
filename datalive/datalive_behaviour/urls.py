from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'behaviour/safety_abc/vehicle_group', views.SafetyABCVehicleViewSet, base_name='behaviour-safety-abc-vehicle-group')
router.register(r'behaviour/safety_mobileeye/vehicle_group', views.SafetyMobileEyeVehicleViewSet, base_name='behaviour-safety-mobileeye-vehicle-group')
urlpatterns = router.urls
