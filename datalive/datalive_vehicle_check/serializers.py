# -*- coding: utf-8 -*-
import uuid
import base64

from django.core.files.base import ContentFile

from rest_framework import serializers

from .models import Damage, Report, QuestionResponse, ReportPhoto, GateCheckReport, \
    AuditSurveyTemplate, AuditSurveyReport
from datalive_cust_veh.serializers import *


def generate_filename(ext='svg'):
    return '{}.{}'.format(uuid.uuid4(), ext).replace('-', '')


def convert_base64_to_file(raw_file):
    if raw_file:
        format, imgstr = raw_file.split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name=generate_filename(ext))
    else:
        return None


class QuestionResponseSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.description', read_only=True)
    answer_text = serializers.CharField(source='answer.answer', read_only=True)

    class Meta:
        model = QuestionResponse
        fields = '__all__'


class DamageSerializer(serializers.ModelSerializer):
    fixed_by = serializers.CharField(source='fixed_by.fullname', read_only=True)
    schemantic = SchematicViewSerializer(required=True)
    class Meta:
        model = Damage
        fields = '__all__'

class DamagePostSerializer(serializers.ModelSerializer):
    fixed_by = serializers.CharField(source='fixed_by.fullname', read_only=True)
    # schemantic = serializers.IntegerField(write_only=True) # accept integer values
    class Meta:
        model = Damage
        fields = '__all__'


class ReportPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPhoto
        fields = '__all__'

class ReportGetSerializer(serializers.ModelSerializer):
    
    photos = ReportPhotoSerializer(read_only=True, many=True)
    new_damage = DamageSerializer(many=True)
    fixed_damage = DamageSerializer(many=True)
    question_responses = QuestionResponseSerializer(many=True)
    
    class Meta:
        model = Report
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):

    photos = ReportPhotoSerializer(read_only=True, many=True)
    new_damage = DamagePostSerializer(many=True)
    fixed_damage = DamagePostSerializer(many=True)
    question_responses = QuestionResponseSerializer(many=True)

    def __init__(self, *args, **kwargs):

        self.photos = []
        self.svg_driver_signature = None
        self.svg_checker_signature = None

        if kwargs.get('data', {}).get('checker_signature', None):
            self.svg_checker_signature = ContentFile(kwargs['data'].pop('checker_signature'))

        if kwargs.get('data', {}).get('driver_signature', None):
            self.svg_driver_signature = ContentFile(kwargs['data'].pop('driver_signature'))

        if kwargs.get('data', {}).get('photos', None):
            photos = kwargs.get('data', {}).get('photos', [])
            for item in photos:
                self.photos.append(convert_base64_to_file(item.get('photo', None)))

        super(ReportSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):

        # self.data['photos'] = []
        self.data['new_damage'] = []
        self.data['fixed_damage'] = []

        # photos = validated_data.pop('photos', None)
        question_responses = validated_data.pop('question_responses', [])
        new_damages = validated_data.pop('new_damage', [])
        fixed_damages = validated_data.pop('fixed_damage', [])

        report = Report.objects.create(**validated_data)

        if self.svg_checker_signature:
            report.checker_signature.save(generate_filename(), self.svg_checker_signature)
        if self.svg_driver_signature:
            report.driver_signature.save(generate_filename(), self.svg_driver_signature)
        if self.photos:
            for item in self.photos:
                report_photo = ReportPhoto.objects.create(photo=item)
                report.photos.add(report_photo)

        for item in new_damages:
            damage = Damage.objects.create(**item)
            report.new_damage.add(damage)

        for item in fixed_damages:
            damage = Damage.objects.create(**item)
            report.fixed_damage.add(damage)

        for item in question_responses:
            response = QuestionResponse.objects.create(**item)
            report.question_responses.add(response)

        return report

    class Meta:
        model = Report
        fields = '__all__'


class GateCheckSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.fullname', read_only=True)
    hub_name = serializers.CharField(source='hub.name', read_only=True)
    depot_name = serializers.CharField(source='depot.name', read_only=True)

    tractor_photos = ReportPhotoSerializer(read_only=True, many=True)
    trailer_photos = ReportPhotoSerializer(read_only=True, many=True)
    hub_photos = ReportPhotoSerializer(read_only=True, many=True)

    tractor_question_responses = QuestionResponseSerializer(many=True)
    trailer_question_responses = QuestionResponseSerializer(many=True)
    hub_question_responses = QuestionResponseSerializer(many=True)

    def __init__(self, *args, **kwargs):

        self.tractor_photos = []
        self.trailer_photos = []
        self.hub_photos = []

        if kwargs.get('data', {}).get('tractor_photos', None):
            tractor_photos = kwargs.get('data', {}).get('tractor_photos', [])
            for item in tractor_photos:
                self.tractor_photos.append(convert_base64_to_file(item.get('photo', None)))

        if kwargs.get('data', {}).get('trailer_photos', None):
            trailer_photos = kwargs.get('data', {}).get('trailer_photos', [])
            for item in trailer_photos:
                self.trailer_photos.append(convert_base64_to_file(item.get('photo', None)))

        if kwargs.get('data', {}).get('hub_photos', None):
            hub_photos = kwargs.get('data', {}).get('hub_photos', [])
            for item in hub_photos:
                self.hub_photos.append(convert_base64_to_file(item.get('photo', None)))

        super(GateCheckSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        tractor_question_responses = validated_data.pop('tractor_question_responses', [])
        trailer_question_responses = validated_data.pop('trailer_question_responses', [])
        hub_question_responses = validated_data.pop('hub_question_responses', [])

        validated_data['user'] = getattr(self.context.get('request'), 'user', None)

        report = GateCheckReport.objects.create(**validated_data)

        if self.trailer_photos:
            for item in self.trailer_photos:
                trailer_photo = ReportPhoto.objects.create(photo=item)
                report.trailer_photos.add(trailer_photo)

        if self.tractor_photos:
            for item in self.tractor_photos:
                tractor_photo = ReportPhoto.objects.create(photo=item)
                report.trailer_photos.add(tractor_photo)

        if self.hub_photos:
            for item in self.hub_photos:
                hub_photo = ReportPhoto.objects.create(photo=item)
                report.hub_photos.add(hub_photo)

        for item in tractor_question_responses:
            response = QuestionResponse.objects.create(**item)
            report.tractor_question_responses.add(response)

        for item in trailer_question_responses:
            response = QuestionResponse.objects.create(**item)
            report.trailer_question_responses.add(response)

        for item in hub_question_responses:
            response = QuestionResponse.objects.create(**item)
            report.hub_question_responses.add(response)

        return report

    class Meta:
        model = GateCheckReport
        fields = '__all__'


class DepotReportSerializer(serializers.ModelSerializer):
    vehicle_reg = serializers.CharField(source='vehicle.registration')
    damages_count = serializers.IntegerField(source='new_damage.count')
    defect_status = serializers.SerializerMethodField()
    outcome = serializers.CharField(source='get_report_class_display')
    user_name = serializers.CharField(source='user.fullname')

    class Meta:
        model = Report
        fields = ('id', 'date', 'time', 'vehicle_reg', 'checker_name', 'driver_name', 'user_name',
                  'damages_count', 'defect_status', 'defect_details', 'notes', 'outcome')

    def get_defect_status(self, obj):
        answer = obj.question_responses.filter(question__description__icontains='has defect').first()
        return answer.answe if answer else ''

class VehicleDamagesSerializer(serializers.ModelSerializer):
    vehicle_reg = serializers.CharField(source='vehicle.registration')
    location = serializers.CharField(source='schemantic.name')
    reported_by = serializers.CharField(source='rep_by.fullname')
    fixed_by = serializers.CharField(source='fixed_by.fullname')

    class Meta:
        model = Damage
        fields = ('id', 'type', 'vehicle_reg', 'location', 'date', 'time', 'reported_by',
                  'fixed_date', 'fixed_by')


class DepotDamagesSerializer(serializers.ModelSerializer):
    vehicle_reg = serializers.CharField(source='vehicle.registration')
    location = serializers.CharField(source='schemantic.name')
    reported_by = serializers.CharField(source='rep_by.fullname')
    fixed_by = serializers.CharField(source='fixed_by.fullname')

    class Meta:
        model = Damage
        fields = ('id', 'type', 'vehicle_reg', 'location', 'date', 'time', 'reported_by',
                  'fixed_date', 'fixed_by')


class ReportDetailsSerializer(serializers.ModelSerializer):
    new_damage_count = serializers.IntegerField(source='new_damage.count')
    status = serializers.CharField(source='get_report_class_display')
    vehicle_reg = serializers.CharField(source='vehicle.registration')
    history = DamageSerializer(source='vehicle.damage_set.all', many=True)
    new_damages = DamageSerializer(source='new_damage', many=True)
    conditions = QuestionResponseSerializer(source='question_responses.all', many=True)
    # livery = LiverySchematic(source='vehicle.livery')

    class Meta:
        model = Report
        fields = ('id', 'date', 'time', 'checker_name', 'checker_signature', 'driver_name',
                  'driver_signature', 'notes', 'odometer', 'defect_details', 'new_damage_count',
                  'status', 'vehicle_reg', 'history', 'conditions', 'new_damages', 'livery')


class AuditSurveyTemplateSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    reports_num = serializers.IntegerField(source='reports.count', read_only=True)

    class Meta:
        model = AuditSurveyTemplate
        fields = '__all__'


class AuditSurveyReportShortSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='created_by.fullname', read_only=True)
    depot_name = serializers.CharField(source='depot.name', read_only=True)

    class Meta:
        model = AuditSurveyReport
        fields = ('id', 'depot', 'added', 'user_name', 'depot_name')


class AuditSurveyReportFullSerializer(AuditSurveyReportShortSerializer):

    class Meta(AuditSurveyReportShortSerializer.Meta):
        fields = AuditSurveyReportShortSerializer.Meta.fields + ('template', 'data')
