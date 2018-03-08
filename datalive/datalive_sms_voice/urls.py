from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from datalive_sms_voice import views

urlpatterns = [
    url(r'^sms/panic-button', views.ReceivePanicButtonMessageView.as_view(), name="panic-button"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
