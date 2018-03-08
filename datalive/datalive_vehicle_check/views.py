# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics, status
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Q

from .models import Report, Damage, GateCheckReport, AuditSurveyTemplate, AuditSurveyReport
from .serializers import ReportSerializer, DepotReportSerializer, DamageSerializer, DepotDamagesSerializer, VehicleDamagesSerializer, ReportDetailsSerializer,\
    GateCheckSerializer, AuditSurveyTemplateSerializer, AuditSurveyReportShortSerializer, AuditSurveyReportFullSerializer
from datalive_cust_veh.models import VehicleGroup, Vehicle
from datalive_auth.permissions import IsCustomer, IsUser, IsVehicle


class VehicleCheck(generics.CreateAPIView):
    permission_classes = (IsUser, )
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # def get_serializer_class(self):
    #     if self.request.method in ('POST', ):
    #         print('POST ReportSerializer')
    #         return ReportSerializer
    #     return ReportGetSerializer

class VehicleDamagesListView(generics.ListAPIView):
    permission_classes = (IsUser, )
    queryset = Damage.objects.all()
    serializer_class = DamageSerializer

    def get_queryset(self):
        print('Vehicle Damages')
        print(self.kwargs)
        qs = super(VehicleDamagesListView, self).get_queryset()
        vehicle = generics.get_object_or_404(Vehicle.objects.all(), id=self.kwargs['vehicle_id'])
       
        return qs.filter(vehicle=vehicle)


class DepotReportListView(generics.ListAPIView):
    permission_classes = (IsCustomer, )
    queryset = Report.objects.all()
    serializer_class = DepotReportSerializer
    # filter_backends = type

    def get_queryset(self):
        qs = super(DepotReportListView, self).get_queryset()
        depot = generics.get_object_or_404(VehicleGroup.objects.all(), id=self.kwargs['depot_id'])
        qs = qs.filter(type=self.request.query_params.get('type', 'STD'))
        if 'start_date' in self.request.query_params and 'end_date' in self.request.query_params:
            try:
                qs = qs.filter(
                    date__range=(
                        datetime.strptime(self.request.query_params['start_date'], '%d-%m-%Y'),
                        datetime.strptime(self.request.query_params['end_date'], '%d-%m-%Y')
                    )
                )
            except Exception as e:
                pass
        return qs.filter(vehicle__in=depot.vehicles.values_list('id', flat=True))


class DepotDamagesListView(generics.ListAPIView):
    permission_classes = (IsCustomer, )
    queryset = Damage.objects.all()
    serializer_class = DepotDamagesSerializer

    def get_queryset(self):
        qs = super(DepotDamagesListView, self).get_queryset()
        depot = generics.get_object_or_404(VehicleGroup.objects.all(), id=self.kwargs['depot_id'])
        if 'start_date' in self.request.query_params and 'end_date' in self.request.query_params:
            try:
                qs = qs.filter(
                    date__range=(
                        datetime.strptime(self.request.query_params['start_date'], '%d-%m-%Y'),
                        datetime.strptime(self.request.query_params['end_date'], '%d-%m-%Y')
                    )
                )
            except Exception as e:
                pass
        return qs.filter(vehicle__in=depot.vehicles.values_list('id', flat=True))


class ReportDetailsView(generics.RetrieveAPIView):
    permission_classes = (IsCustomer, )
    queryset = Report.objects.all()
    serializer_class = ReportDetailsSerializer


class DepotGateCheckListView(generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    permission_classes = (IsCustomer, )
    queryset = GateCheckReport.objects.all()
    serializer_class = GateCheckSerializer

    def get(self, request, *args, **kwargs):
        if 'depot_id' in self.kwargs:
            return self.list(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(DepotGateCheckListView, self).get_queryset()

        if 'pk' in self.kwargs:
            return qs

        if 'depot_id' not in self.kwargs:
            return qs.none()

        depot = generics.get_object_or_404(VehicleGroup.objects.all(), id=self.kwargs['depot_id'])
        if 'start_date' in self.request.query_params and 'end_date' in self.request.query_params:
            try:
                qs = qs.filter(
                    date__range=(
                        datetime.strptime(self.request.query_params['start_date'], '%d-%m-%Y'),
                        datetime.strptime(self.request.query_params['end_date'], '%d-%m-%Y')
                    )
                )
            except Exception as e:
                pass
        return qs.filter(depot=depot)


class AuditSurveyTemplateListView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = (IsCustomer, )
    serializer_class = AuditSurveyTemplateSerializer

    def get_queryset(self):
        if self.request.user.permission.is_global_admin:
            return AuditSurveyTemplate.objects.all()
        else:
            return AuditSurveyTemplate.objects.filter(
                customer__in=self.request.user.customers.values_list('id', flat=True))

    def perform_create(self, serializer):
        if serializer.validated_data.get('is_default'):
            customer_templates = AuditSurveyTemplate.objects.filter(customer=serializer.validated_data.get('customer'))
            customer_templates.update(is_default=False)
        template = serializer.save()
        template.created_by = self.request.user
        template.save()


class AuditSurveyTemplateDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = (IsCustomer, )
    serializer_class = AuditSurveyTemplateSerializer

    def get_object(self):
        return generics.get_object_or_404(AuditSurveyTemplate, id=self.kwargs['pk'])

    def perform_update(self, serializer):
        if serializer.validated_data.get('is_default'):
            customer_templates = AuditSurveyTemplate.objects.filter(customer=serializer.instance.customer)
            customer_templates.update(is_default=False)
        serializer.save()


class AuditSurveyReportListView(generics.CreateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView, generics.ListAPIView):
    permission_classes = (IsCustomer, )

    def get_queryset(self):
        tpl_id = self.request.query_params.get('tpl_id')
        if self.request.user.permission.is_global_admin:
            qs = AuditSurveyReport.objects.all()
        else:
            qs = AuditSurveyReport.objects.filter(
                template__customer__in=self.request.user.customers.values_list('id', flat=True)).distinct()

        return qs if not tpl_id else qs.filter(template=tpl_id)

    def get_serializer_class(self):
        if self.lookup_field in self.kwargs or self.request.method == 'POST':
            return AuditSurveyReportFullSerializer
        else:
            return AuditSurveyReportShortSerializer

    def perform_create(self, serializer):
        report = serializer.save()
        report.created_by = self.request.user
        report.save()

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, args, kwargs)
        else:
            return self.list(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        print self.request.query_params
        if 'ids' in self.request.query_params:
            ids = self.request.query_params['ids'].split(',')
            AuditSurveyReport.objects.filter(id__in=ids).delete()
            return Response({'message': 'success'}, status=status.HTTP_200_OK)


class AuditSurveyTemplateCustomerView(generics.RetrieveAPIView):
    permission_classes = (IsCustomer, )
    serializer_class = AuditSurveyTemplateSerializer

    def get_object(self):
        customer_id = self.request.query_params.get('id')
        if customer_id:
            customer = self.request.user.customers.filter(id=customer_id).first()
        else:
            customer = self.request.user.customers.first()
        return generics.get_object_or_404(AuditSurveyTemplate, customer=customer, is_default=True)
