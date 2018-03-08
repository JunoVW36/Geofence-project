from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
   url(r'^vehicle-check/', views.VehicleCheck.as_view(), name="vehicle-check"),
   url(r'^depot_report/(?P<depot_id>[0-9]+)/$', views.DepotReportListView.as_view(), name="depot-report-list"),
   url(r'^vehicle_damages/(?P<vehicle_id>[0-9]+)/$', views.VehicleDamagesListView.as_view(), name="vehicle-damages-list"),
   url(r'^depot_damages/(?P<depot_id>[0-9]+)/$', views.DepotDamagesListView.as_view(), name="depot-damages-list"),
   url(r'^depot_gatecheck/$', views.DepotGateCheckListView.as_view(), name="depot-gatecheck-create"),
   url(r'^depot_gatecheck/(?P<depot_id>[0-9]+)/$', views.DepotGateCheckListView.as_view(), name="depot-gatecheck-list"),
   url(r'^gatecheck_details/(?P<pk>[0-9]+)/$', views.DepotGateCheckListView.as_view(), name="depot-gatecheck-details"),
   url(r'^report_details/(?P<pk>[0-9]+)/$', views.ReportDetailsView.as_view(), name="report-details"),
   url(r'^audit_survey_template/$', views.AuditSurveyTemplateListView.as_view(), name="audit-survey-template-list"),
   url(r'^audit_survey_template/(?P<pk>[0-9]+)/$', views.AuditSurveyTemplateDetailView.as_view(), name="audit-survey-template-detail"),
   url(r'^audit_survey_template/customer/$', views.AuditSurveyTemplateCustomerView.as_view(), name="audit-survey-template-customer"),
   url(r'^audit_survey_report/$', views.AuditSurveyReportListView.as_view(), name="audit-survey-report-list"),
   url(r'^audit_survey_report/(?P<pk>[0-9]+)/$', views.AuditSurveyReportListView.as_view(), name="audit-survey-report-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
