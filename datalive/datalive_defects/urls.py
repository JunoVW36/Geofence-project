from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^defect/fault/', views.FaultListView.as_view(), name="equipment-list"),
    url(r'^defect/equipment/', views.EquipmentListView.as_view(), name="equipment-list"),
    url(r'^defect/', views.DefectListCreate.as_view(), name="defect-list"),
    

]

urlpatterns = format_suffix_patterns(urlpatterns)
