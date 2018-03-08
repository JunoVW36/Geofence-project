# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from datetime import date, timedelta
from collections import OrderedDict
from django.db import models

from .models import *
from datalive_vehicle_check.models import Report, Damage


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    class Meta:
        model = Contact
        fields = '__all__'

class DriverCategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverCategory
        # fields = '__all__'
        fields = ['id', 'display_name', 'category']
    
class DriverCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverCategory
        fields = '__all__'
        
class InsurancePolicyNumberSerializer(serializers.ModelSerializer):
    vehicle_category = DriverCategoryNameSerializer(required=False)
    class Meta:
        model = InsurancePolicyNumber
        fields = ['id', 'name', 'policy_document', 'policy_number', 'vehicle_category']


class InsuranceSerializer(serializers.ModelSerializer):
    policies = InsurancePolicyNumberSerializer(source='get_policy_numbers',required=False, many=True, read_only=True)
    # serializers.SerializerMethodField(required=False, read_only=True)

    # def get_insurance_policy_number(self, instance):
    #     serializer = InsurancePolicyNumberSerializer(instance=instance., required=False, many=True)
    #     return serializer.data
    class Meta:
        model = Insurance
        fields = '__all__'

class LiveryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveryCategory
        fields = '__all__'

class SchematicViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchematicView
        fields = ['name', 'view_name', 'img']


class LiverySchematicSerializer(serializers.ModelSerializer):
    views = SchematicViewSerializer(many=True)
    class Meta:
        model = LiverySchematic
        fields = ['id', 'manufacturer_model', 'hero_image', 'views', 'customer' ]



class FAQActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQActions
        fields = '__all__'


class FAQDescriptionSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField(required=False, read_only=True)
    def get_actions(self, instance):
        serializer = FAQActionsSerializer(instance=instance.actions, required=False, many=True)
        return serializer.data

    class Meta:
        model = FAQDescription
        fields = '__all__'
        # fields = ['description', 'actions']'__all__'


class FAQSerializer(serializers.ModelSerializer):
    driver_category = DriverCategoryNameSerializer(required=False)
    description = FAQDescriptionSerializer(source='get_faq_description',required=False, many=True, read_only=True)
    class Meta:
        model = FAQ
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    faq = FAQSerializer(source='get_faq',required=False, many=True, read_only=True)
    insurance = InsuranceSerializer(source='get_insurance', required=False)
    contacts = ContactSerializer(required=False)
    maintenance_control = ContactSerializer(required=False)
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerSerializerMinimal(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']


class VehicleTrackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleTracker
        fields = '__all__'


class LeaseCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaseCompany
        fields = '__all__'

class VehicleGroupForVehicleSerializer(serializers.ModelSerializer):
    vehicle_group_contacts = serializers.SerializerMethodField(required=False)

    def get_vehicle_group_contacts(self, instance):
        serializer = VehicleGroupContactSerializer(instance=instance.vehicle_group_contacts, required=False, many=True)
        return serializer.data

    class Meta:
        model = VehicleGroup
        fields = ['name', 'description', 'vehicle_group_contacts', 'is_depot', 'is_hub', 'is_linehaul']


class VehicleGroupSerializer(serializers.ModelSerializer):
    vehicles = serializers.SerializerMethodField(required=False, read_only=True)
    # TODO - check to see if this customer need all FAQ json data in return json
    customer = CustomerSerializerMinimal(required=False)
    #TODO - Check is users are needed on VehicleGroup Serializer??
    users = serializers.SerializerMethodField(required=False)
    vehicle_group_contacts = serializers.SerializerMethodField(required=False)
    def get_users(self, instance):
        from datalive_auth.serializers import DataliveUserSmallSerializer
        serializer = DataliveUserSmallSerializer(instance=instance.user_vehicle_groups, required=False, many=True)
        return serializer.data

    def get_vehicles(self, instance):
        serializer = VehicleListSerializer(instance=instance.vehicles, required=False, many=True)
        return serializer.data

    def get_vehicle_group_contacts(self, instance):
        serializer = VehicleGroupContactSerializer(instance=instance.vehicle_group_contacts, required=False, many=True)
        return serializer.data

    def create(self, validated_data):
        vehicles = self.initial_data.pop('vehicles')
        vehicles = [vehicle['id'] for vehicle in vehicles]
        customer_name = self.initial_data.pop('new_customer')
        vehicle_group = VehicleGroup.objects.create(**self.initial_data)
        vehicle_group.customer = Customer.get_by_name(customer_name)
        vehicle_group.save()

        vehicles_list = Vehicle.objects.filter(id__in=vehicles)
        vehicle_group.vehicles.add(*vehicles_list)
        return vehicle_group


    class Meta:
        model = VehicleGroup
        fields = '__all__'


class VehicleGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleGroup
        fields = ['id', 'name', 'creation_datetime']



class VehicleGroupContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    class Meta:
        model = VehicleGroupContact
        fields = '__all__'


class VehicleManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleManufacturer
        fields = '__all__'


class VehicleManufacturerModelSerializer(serializers.ModelSerializer):
    # manufacturer = SerializerMethodField(required=False)
    manufacturer = VehicleManufacturerSerializer(required=True)
    vehicle_model_contacts = VehicleGroupContactSerializer(required=False, many=True)
    schematics = SchematicViewSerializer(required=False, many=True)
    
    def get_manufacturer(self, instance):
        serializer = VehicleManufacturerSerializer(instance=instance.manufacturer, required=False)
        name = serializer.data['name']
        return name

    class Meta:
        model = VehicleManufacturerModel
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    manufacturer_model = VehicleManufacturerModelSerializer(required=False)
    driver_category = DriverCategorySerializer(required=False)
    trackers = VehicleTrackerSerializer(required=False, many=True, read_only=True)
    vehicle_groups = VehicleGroupUserSerializer(required=False, many=True, read_only=True) 
    lease_company = LeaseCompanySerializer(required=False)
    customer = CustomerSerializerMinimal(required=False)
    livery_category = LiveryCategorySerializer(required=False)
    livery_schematic = SerializerMethodField(required=False, read_only=True) # only a GET field

    def get_livery_schematic(self, obj):
        """gets the customers livery schematics the vehicle"""
        livery = obj.livery_category
        if livery:
            model = obj.manufacturer_model.model
            customer = obj.customer
            print(model, livery, customer)
            try:
                qs = LiverySchematic.objects.get(livery_category=livery, manufacturer_model__model=model, customer=customer)
                schematic = LiverySchematicSerializer(instance=qs).data
            except LiverySchematic.DoesNotExist:
                schematic = None           
            return schematic
        else:
            return None   
        

    def create(self, validated_data):
        trackers = self.initial_data.pop('trackers')
        customer_name = self.initial_data.pop('new_customer')
        vehicle = Vehicle.objects.create(**self.initial_data)
        vehicle.customer = Customer.get_by_name(customer_name)
        vehicle.save()

        tracker_ids = [tracker['id'] for tracker in trackers]
        trackers = VehicleTracker.objects.filter(id__in=tracker_ids)
        for tracker in trackers:
            vehicle.trackers.add(tracker) if tracker else None
        return vehicle


    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleListSerializer(serializers.ModelSerializer):
    vehicle_type = SerializerMethodField(required=False)

    def get_vehicle_type(self, instance):
        serializer = VehicleManufacturerModelSerializer(instance=instance.manufacturer_model, required=False)
        # Note in the following that the RRset model has a `domain` foreign-key field which is referenced here. It is irrelevant for the current problem though.
        type = serializer.data['vehicle_type']
        if type is not None:
            return type
        else:
            return 'VAN'


    class Meta:
        model = Vehicle
        fields = ['id', 'registration', 'creation_datetime', 'vehicle_type']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'VehicleGroup']


class RegionListSerializer(serializers.ModelSerializer):
    vehicle_groups = SerializerMethodField()

    class Meta:
        model = Region
        fields = ['id', 'name', 'vehicle_groups']

    def get_vehicle_groups(self, region):
        user = getattr(self.context.get('request'), 'user', None)

        if user.permission.is_global_admin:
            qs = region.VehicleGroups.all()
        elif user.permission.is_customer:
            qs = region.VehicleGroups.filter(customer__id__in=user.customers.all().values_list('id', flat=True))
        elif user.permission.is_user:
            qs = region.VehicleGroups.filter(id__in=user.vehicle_groups.values_list('id', flat=True))
        else:
            qs = VehicleGroup.objects.none()

        return VehicleGroupUserSerializer(instance=qs, many=True).data


class RegionDepotsStatsSerializer(serializers.ModelSerializer):
    vehicles = serializers.IntegerField(source='vehicles_num')

    class Meta:
        model = VehicleGroup
        fields = ['id', 'name', 'vehicles', 'num_damaged_vehicles', 'num_damaged_vehicles_over_21_days']


class RegionStatsSerializer(serializers.ModelSerializer):
    total_vehicles = SerializerMethodField()
    total_damaged_vehicles = SerializerMethodField()
    num_damages_not_fixed = SerializerMethodField()
    num_damages_not_fixed_over_21_days = SerializerMethodField()
    total_damages = SerializerMethodField()
    total_vehicle_checks = SerializerMethodField()
    total_handovers = SerializerMethodField()
    total_audit_checks = SerializerMethodField()

    class Meta:
        model = Region
        fields = ['total_vehicles', 'total_damaged_vehicles', 'num_damages_not_fixed',
                  'num_damages_not_fixed_over_21_days', 'total_damages',
                  'total_vehicle_checks', 'total_handovers', 'total_audit_checks']

    def get_filter_params(self):
        user = getattr(self.context.get('request'), 'user', None)

        if user.permission.is_global_admin:
            return {}
        elif user.permission.is_customer:
            return {'customer__id__in': user.customers.all().values_list('id', flat=True)}
        elif user.permission.is_user:
            return {'id__in': user.vehicle_groups.values_list('id', flat=True)}
        else:
            # to return empty qs if user doesn't have permissions
            return {'name__isnull': True}

    def get_total_vehicles(self, region):
        return region.VehicleGroups.filter(**self.get_filter_params()).annotate(
            vehicles_num=models.Count('vehicles')
        ).aggregate(total=models.Sum('vehicles_num'))['total']

    def get_total_damaged_vehicles(self, region):
        return Vehicle.objects.filter(
            id__in=region.VehicleGroups.filter(**self.get_filter_params()).values_list('vehicles', flat=True)
        ).annotate(
            damages_num=models.Sum(
                models.Case(
                    models.When(damage__status='NEW', then=1),
                    default=0,
                    output_field=models.IntegerField()
                )
            )
        ).filter(damages_num__gt=0).count()

    def get_num_damages_not_fixed(self, region):
        return Vehicle.objects.filter(
            id__in=region.VehicleGroups.filter(**self.get_filter_params()).values_list('vehicles', flat=True)
        ).annotate(
            damages_num=models.Sum(
                models.Case(
                    models.When(damage__status='NEW', then=1),
                    default=0,
                    output_field=models.IntegerField()
                )
            )
        ).aggregate(total=models.Sum('damages_num'))['total']

    def get_total_damages(self, region):
        return Vehicle.objects.filter(
            id__in=region.VehicleGroups.filter(**self.get_filter_params()).values_list('vehicles', flat=True)
        ).annotate(
            damages_num=models.Count('damage')
        ).aggregate(total=models.Sum('damages_num'))['total']

    def get_num_damages_not_fixed_over_21_days(self, region):
        return Vehicle.objects.filter(
            id__in=region.VehicleGroups.values_list('vehicles', flat=True)
        ).annotate(
            damages_num=models.Sum(
                models.Case(
                    models.When(damage__status='NEW',
                                damage__date__lt=date.today() - timedelta(days=21),
                                then=1),
                    default=0,
                    output_field=models.IntegerField()
                )
            )
        ).aggregate(total=models.Sum('damages_num'))['total']

    def get_total_vehicle_checks(self, region):
        return region.get_all_reports_queryset(self.get_filter_params()).filter(type='STD').count()

    def get_total_handovers(self, region):
        return region.get_all_reports_queryset(self.get_filter_params()).filter(type='HND').count()

    def get_total_audit_checks(self, region):
        return region.get_all_reports_queryset(self.get_filter_params()).filter(type='AUD').count()


class DepotStatsSerializer(serializers.ModelSerializer):
    daily_stats = serializers.SerializerMethodField()
    total_damages = serializers.SerializerMethodField()
    fixed_damages = serializers.SerializerMethodField()
    num_checks = serializers.SerializerMethodField()
    num_audits = serializers.SerializerMethodField()
    num_handovers = serializers.SerializerMethodField()

    class Meta:
        model = VehicleGroup
        fields = ('id', 'name', 'total_damages', 'fixed_damages', 'num_checks', 'num_audits',
                  'num_handovers', 'daily_stats')

    def __init__(self, *args, **kwargs):
        super(DepotStatsSerializer, self).__init__(*args, **kwargs)
        self.start_date = self.context.get('start_date')
        self.end_date = self.context.get('end_date')
        vehicle_ids = self.instance.vehicles.values_list('id', flat=True)
        if self.start_date and self.end_date:
            self.reports = Report.objects.filter(vehicle__in=vehicle_ids, date__range=(self.start_date, self.end_date))
            self.damages = Damage.objects.filter(vehicle__in=vehicle_ids, date__range=(self.start_date, self.end_date))
        else:
            self.reports = Report.objects.filter(vehicle__in=vehicle_ids)
            self.damages = Damage.objects.filter(vehicle__in=vehicle_ids)

    def get_total_damages(self, obj):
        return self.damages.filter(
            date__range=(self.start_date, self.end_date)
        ).count() if self.start_date and self.end_date else self.damages.count()

    def get_fixed_damages(self, obj):
        qs = self.damages.filter(status='FIX')
        return qs.filter(
            date__range=(self.start_date, self.end_date)
        ).count() if self.start_date and self.end_date else qs.count()

    def get_num_checks(self, obj):
        qs = self.reports.filter(type='STD')
        return qs.filter(
            date__range=(self.start_date, self.end_date)
        ).count() if self.start_date and self.end_date else qs.count()

    def get_num_audits(self, obj):
        qs = self.reports.filter(type='AUD')
        return qs.filter(
            date__range=(self.start_date, self.end_date)
        ).count() if self.start_date and self.end_date else qs.count()

    def get_num_handovers(self, obj):
        qs = self.reports.filter(type='HND')
        return qs.filter(
            date__range=(self.start_date, self.end_date)
        ).count() if self.start_date and self.end_date else qs.count()

    def get_daily_stats(self, obj):
        # vehicles checked - num of vehicles which has report object added on date by X axes
        # vehicles unchecked - it can be calculated as (num_total_vehicles - num_vehicles_checked)

        unique_vehicles = OrderedDict()
        checked_vehicles = OrderedDict()
        total_vehicles = OrderedDict()

        for report in self.reports.order_by('date'):
            date_txt = report.date.strftime('%b %d')
            if date_txt not in checked_vehicles:
                checked_vehicles[date_txt] = 1
                total_vehicles[date_txt] = Vehicle.objects.filter(
                    vehiclegroup__in=[obj.id], creation_datetime__lte=report.date).count()
                unique_vehicles[date_txt] = [report.vehicle_id]
            elif report.vehicle_id not in unique_vehicles[date_txt]:
                checked_vehicles[date_txt] += 1
                unique_vehicles[date_txt].append(report.vehicle_id)

        return [
            {
                'date': key,
                'num_checked': checked_vehicles[key],
                'num_unchecked': total_vehicles[key] - checked_vehicles[key]
            } for key in checked_vehicles.keys()
        ]
