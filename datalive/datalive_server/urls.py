from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^server/auth/test/',views.ServerTokenAuthTest.as_view(), name="server-auth-test"),
    url(r'^server/auth/defect/', views.DefectListCreate.as_view(), name="server-defect"),
    url(r'^server/auth/vehiclecheck/', views.VehicleCheckListCreate.as_view(), name="server-vehicle-check"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
