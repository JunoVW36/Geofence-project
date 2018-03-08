from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from datalive_notifications import views

urlpatterns = [
    url(r'^notification/', views.NotificationListCreate.as_view(), name="notification-list"),
    url(r'daily_vehicle_check_damage_email', views.VehicleCheckDamage.as_view(), name="vehicle-check-damage-email"),
    url(r'mot_expiry_email_notifications', views.MotExpiryEmail.as_view(), name="mot-expiry-email"),
]

urlpatterns = format_suffix_patterns(urlpatterns)