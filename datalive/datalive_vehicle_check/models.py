# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_mysql.models import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from datalive_cust_veh.models import Customer, VehicleGroup, Vehicle, SchematicView
from datalive_auth.models import DataliveUser


def validate_gatecheck_hub(value):
    if not value.is_hub:
        raise ValidationError(
            _('%(value)s should be is_hub == True'),
            params={'value': value},
        )


def validate_gatecheck_depot(value):
    if not value.is_depot:
        raise ValidationError(
            _('%(value)s should be is_depot == True'),
            params={'value': value},
        )

# Questions are what XLR refered to as 'flags'

# Predefined answers to questions (eg. 'YES', 'NO', '1 Set', '2 Sets')
class QuestionDefinitionAnswer(models.Model):
    answer = models.CharField(max_length=128)

    def __str__(self):
        return self.answer


# Predefined questions (eg. 'Vehicle clean?')
class QuestionDefinition(models.Model):
    QUESTION_VEHICLE_TYPE = 'vehicle'
    QUESTION_TRACTOR_TYPE = 'tractor'
    QUESTION_TRAILER_TYPE = 'trailer'
    QUESTION_HUB_TYPE = 'hub'

    QUESTION_TYPE_CHOICES = (
        (QUESTION_VEHICLE_TYPE, 'Vehicle Condition'),
        (QUESTION_TRACTOR_TYPE, 'Tractor Condition'),
        (QUESTION_TRAILER_TYPE, 'Trailer Condition'),
        (QUESTION_HUB_TYPE, 'Hub Condition'),
    )

    type = models.CharField(max_length=8, choices=QUESTION_TYPE_CHOICES, default=QUESTION_VEHICLE_TYPE)
    index = models.IntegerField()  # only required to link old XLR fields
    description = models.CharField(max_length=128)
    answers = models.ManyToManyField(QuestionDefinitionAnswer)

    def __str__(self):
        return self.description


# Question responses entered by a user (eg. 'Vehicle clean?', 'Yes')
class QuestionResponse(models.Model):
    question = models.ForeignKey(QuestionDefinition)
    answer = models.ForeignKey(QuestionDefinitionAnswer)

    def __str__(self):
        return str(self.question)

#Damage
class Damage(models.Model):
    VEHICLE_DEFFECTS = (
        ('scratch', 'Scratch'),
        ('crack', 'Crack'),
        ('missing', 'Missing'),
        ('dent', 'Dent'), 
    )
    DAMAGE_STATUS = (
        ('NEW', 'New damage'),
        ('FIX', 'Fixed damage'),
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=10, choices=VEHICLE_DEFFECTS)
    schemantic = models.ForeignKey(SchematicView, on_delete=models.SET_NULL, null=True)
    rep_by = models.ForeignKey(DataliveUser, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    x = models.FloatField(max_length=10, null=True, blank=True)
    y = models.FloatField(max_length=10, null=True, blank=True)
    bx = models.FloatField(max_length=10, null=True, blank=True)
    by = models.FloatField(max_length=10, null=True, blank=True)
    bw = models.FloatField(max_length=10, null=True, blank=True)
    bh = models.FloatField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=5, choices=DAMAGE_STATUS, default='NEW')
    been_fixed = models.BooleanField(default=False)
    fixed_date = models.DateTimeField(blank=True, null=True)
    fixed_by = models.ForeignKey(DataliveUser, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='fixed_damages')

    def __str__(self):
        return str(self.id)
        #'{}'.format(self.id)



#Report Photos
class ReportPhoto(models.Model):
    """Model to hold all photos uploaded for a vehicle check report
    """
    photo = models.ImageField(upload_to='vehicle-check/photos/%Y/%m/%d/')

    def __str__(self):
        return str(self.id)



# Can use this to upload files to specific folders
# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.user.id, filename)

# class MyModel(models.Model):
#     upload = models.FileField(upload_to=user_directory_path)
def report_id_folder_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.vehicle.id)






# Reports
class Report(models.Model):
    """Model to hold vehicle checks.
    """
    CHECK_TYPE = (
        ('STD', 'Standard Vehicle Check Complete'),
        ('AUD', 'Auditor Vehicle Check of Vehicle'),
        ('HND', 'ODF handover check'),
    )
    REPORT_CLASS = (
        ('CHK', 'Vehicle Check Complete'),
        ('SHOP', 'Not Checked - Vehicle in workshop'),
        ('ROAD', 'Not Checked - Vehicle on the road'),
        ('DEPOT', 'Not Checked - Vehicle at other depot'),
    )
    date = models.DateField(auto_now_add=True, db_index=True)
    time = models.TimeField(auto_now_add=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=5, choices=CHECK_TYPE, default='STD')
    report_class = models.CharField(max_length=5, choices=REPORT_CLASS, default='CHK')
    user = models.ForeignKey(DataliveUser, on_delete=models.SET_NULL, null=True)
    checker_name = models.CharField(max_length=200, null=True) # from old structure - "print_name": "John Smith",	
    checker_signature = models.FileField(upload_to='vehicle-check/signatures/%Y/%m/%d/signature/', null=True)  # from old structure - "signature": "<svg..."
    driver_name = models.CharField(max_length=200, null=True) # from old structure - "driver_signature": "<svg...",	// Full SVG data of signature
    driver_signature = models.FileField(upload_to='vehicle-check/signatures/%Y/%m/%d/signature/', null=True)  # from old structure - 	"driver_print_name": "Fred Bloggs"
    notes = models.TextField(max_length=700, blank=True, null=True)
    photos = models.ManyToManyField(ReportPhoto, blank=True)
    new_damage = models.ManyToManyField(Damage, blank=True, related_name='new_damages')
    fixed_damage = models.ManyToManyField(Damage, blank=True, related_name='fixed_damages')
    odometer = models.IntegerField(blank=True, null=True)
    depot = models.ForeignKey(VehicleGroup, on_delete=models.SET_NULL, null=True)
    defect_details = models.TextField(max_length=700, blank=True, null=True)
    send_email_flag = models.BooleanField(default=True)
    question_responses = models.ManyToManyField(QuestionResponse, related_name='reports')
    # flags ???? replaced with 'questions'
    # "flags": [
    # 		null, null, 1, 1, 0, 1...	// All toggle buttons on vehicle checks register an entry in this list at a certain index
    # 	],

    def __str__(self):
        return self.report_class


class GateCheckReport(models.Model):
    hub = models.ForeignKey(VehicleGroup, on_delete=models.SET_NULL, null=True, related_name="hub_gatecheck_reports") # validators=[validate_gatecheck_hub]
    depot = models.ForeignKey(VehicleGroup, on_delete=models.SET_NULL, null=True, related_name="depot_gatecheck_reports") # validators=[validate_gatecheck_depot]
    date = models.DateField(auto_now_add=True, db_index=True)
    time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(DataliveUser, on_delete=models.SET_NULL, null=True)
    agency = models.NullBooleanField()

    driver_name = models.CharField(max_length=200, null=True)

    reg = models.CharField(max_length=20)
    trailer = models.CharField(max_length=20, null=True, blank=True)

    tractor_photos = models.ManyToManyField(ReportPhoto, null=True, related_name="tractor_gatecheck_reports")
    trailer_photos = models.ManyToManyField(ReportPhoto, null=True, related_name="trailer_gatecheck_reports")
    hub_photos = models.ManyToManyField(ReportPhoto, null=True, related_name="hub_gatecheck_reports")

    tractor_question_responses = models.ManyToManyField(QuestionResponse, related_name='tractor_gatecheck_reports')
    trailer_question_responses = models.ManyToManyField(QuestionResponse, related_name='trailer_gatecheck_reports')
    hub_question_responses = models.ManyToManyField(QuestionResponse, related_name='hub_gatecheck_reports')

    notes = models.TextField(max_length=700, blank=True, null=True)


class AuditSurveyTemplate(models.Model):
    created_by = models.ForeignKey(DataliveUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    customer = models.ForeignKey(Customer, related_name='audit_templates')
    is_default = models.BooleanField(default=False)

    template = JSONField()


class AuditSurveyReport(models.Model):
    template = models.ForeignKey(AuditSurveyTemplate, related_name='reports')
    depot = models.ForeignKey(VehicleGroup, related_name='audit_reports')
    created_by = models.ForeignKey(DataliveUser, on_delete=models.SET_NULL, null=True)
    added = models.DateTimeField(auto_now_add=True)
    data = JSONField()




# # THIS IS THE OLD FORMAT OF VEHCILE CHECK FROM XLR
# This is the XLRNT data structure relevant to Vehicle Check app. The following JSON structures are used when communicating with the app, mostly mimics the internal database structure.

# # Vehicle

# {
# 	"id": "YK64NHG",
# 	"livery": "13",			// Which schematics to use for vehicle checks
# 	"depot": "26",
# 	"alloc": "",
# 	"mot": "30/01/2018",
# 	"ved": "30/09/2017",
# 	"odf": true,			// Changes frequency of checks and displayed on the frontend
# 	"odometer": {
# 		"reading": "47756",
# 		"unit": "miles",
# 		"required": false	// If set, users have to fill it in on every check
# 	}
# }

# # Depot

# {
# 	"id": "26",
# 	"name": "Depot name",
# 	"manager_email": [
# 		"john.smith@example.com",
# 		"fred.bloggs@example.com"
# 	],
# 	"alt_ref": "12"			// Used for syncing with SolarVista
# 	"is_depot": true,
# 	"is_hub": false,
# 	"is_linehaul": true
# }

# # Region
# - Groups depots for the dashboard

# {
# 	"id": "26",
# 	"name": "North West",
# 	"manager_email": ["john.smith@example.com", "fred.bloggs@example.com"],
# 	"alt_ref": "12",
# 	"depot": ["26", "12", "34"]
# }

# # Livery
# - Vehicle schematics

# {
# 	"id": "13"
# 	"livery": "DPD",
# 	"make": "Mercedes",
# 	"model": "Vito",
# 	"views": [
# 		{
# 			"name": "front",
# 			"img": "Mercedes_Vito_Front.jpg"
# 		},
# 		{
# 			"name": "driver",
# 			"img": "Mercedes_Vito_Driver.jpg"
# 		},
# 		{
# 			"name": "back",
# 			"img": "Mercedes_Vito_Back.jpg"
# 		},
# 		{
# 			"name": "passenger",
# 			"img": "Mercedes_Vito_Passenger.jpg"
# 		}
# 	]
# }

# # Damage
# - Damages reported (placed on schematics)

# {
# 	"id": "34051",
# 	"vehicle": "YK64NHG",
# 	"type": "dent",				// Which icon to show
# 	"view": "driver",			// Which image to show on (see livery)
# 	"rep_by": "york.user1",		// Reported by
# 	"date": "30/06/2016",
# 	"time": "08:24",
# 	"x": 35.27,					// Position (in % of image dimensions)
# 	"y": 60.85,
# 	"bx": 0,					// Optional bounding box for area damages (in % of image dimensions)
# 	"by": 0,
# 	"bw": 0,					// Area width
# 	"bh": 0						// Area height
# }

# # Reports
# - All reports are stored in this table under different types

# {
# 	"id": "12",
# 	"date": "01/08/2017",
# 	"time": "11:56:12",
# 	"vehicle": "YK64NHG",
# 	"type": "C",
# 	"user_id": "york.user1",
# 	"signature": "<svg...",			// Full SVG data of signature
# 	"notes": "",
# 	"photo": ["1235", "1236"],		// List of uploaded photos
# 	"new_dmg": ["56", "57"],		// List of new damages reported
# 	"odometer": "",					// Odometer reading
# 	"flags": [
# 		null, null, 1, 1, 0, 1...	// All toggle buttons on vehicle checks register an entry in this list at a certain index
# 	],
# 	"depot": "26",
# 	"print_name": "John Smith",
# 	"driver_signature": "<svg...",	// Full SVG data of signature
# 	"driver_print_name": "Fred Bloggs",
# 	"defect_details": "Notes",
# 	"fixed_dmg": ["12", "35"],		// List of damages fixed
# 	"send_email": true				// Flag for our email sender, set to false once email has been sent
# }

# # Report flags
# - Gives meaning to the report flags array

# {
# 	"index": 5,						// Index in Reports.flags array
# 	"description": "Vehicle clean",
# 	"answers": ["Yes", "No"]
# }

# # Users

# {
# 	"username": "york.user1",
# 	"password": "hash",
# 	"role": "USER",
# 	"depots": [],					// Limit user access to specific depots (unlimited if empty)
# 	"regions": []					// Limit user access to specific regions (unlimited if empty)
# }
