# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datalive_cust_veh.models import Customer, VehicleGroup, Vehicle
from datalive_auth.models import DataliveUser

# Create your models here.


# Predefined faults for equipment (eg. 'no audio', 'No mic', 'Button broken')
class EquipmentDefinitionFault(models.Model):
    fault = models.CharField(max_length=128)
    description = models.TextField(max_length=500)
    """Free txt field for user to add a description of the fault."""
    solar_vista_ref = models.IntegerField(blank=True, null=True)
    """Solar Vista reference. for use when adding items into Solar Vista API"""
    def __str__(self):
        return self.fault

# Predefined Equipments (eg. 'Cab Phone')
class EquipmentDefinition(models.Model):
    xlr_index = models.IntegerField(blank=True, null=True)  # only required to link old XLR fields
    equipment_name = models.CharField(max_length=128)
    faults = models.ManyToManyField(EquipmentDefinitionFault)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    """A Equipment belongs to a single Customer.
    Allow null on delete so that equipments don't accidently get deleted when an Customer gets deleted.
    """
    def __str__(self):
        return self.equipment_name

# Fault of the equipment chosen by a user (eg. 'Cab phone', 'Broken button')
class EquipmentResponse(models.Model):
    equipment = models.ForeignKey(EquipmentDefinition)
    fault = models.ForeignKey(EquipmentDefinitionFault)  
    def __str__(self):
        return str(self.fault)
   


# class Equipment(models.Model):
#     """Model to hold a group of EquipmentFaults.
#     Equipment can have many equipment faults assigned to it.
#     """
#     creation_datetime = models.DateTimeField(auto_now_add=True)
#     name = models.CharField(max_length=200, db_index=True)
#     """Name of equipment shown to user in UI."""
#     description = models.TextField(max_length=500)
#     """Free txt field for user to add a description of the equipment."""
#     customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
#     """A Equipment belongs to a single Customer.
#     Allow null on delete so that equipments don't accidently get deleted when an Customer gets deleted.
#     """
#     depot = models.ForeignKey(VehicleGroup, on_delete=models.SET_NULL, null=True)
#     solar_vista_ref = models.IntegerField(blank=True, null=True)
#     """Solar Vista reference. for use when adding items into Solar Vista API"""

#     def __str__(self):
#         return self.name


# class EquipmentFault(models.Model):
#     """Model to represent a fault of a Equipment.
#     A Fault is an issue of a vehicle equipment.
#     """
#     name = models.CharField(max_length=200, db_index=True)
#     """Name of equipment fault shown to user in main UI."""
#     description = models.TextField(max_length=500)
#     """Free txt field for user to add a description of the fault."""
#     solar_vista_ref = models.IntegerField(blank=True, null=True)
#     """Solar Vista reference. for use when adding items into Solar Vista API"""
#     equipment = models.ForeignKey(Equipment)
#     """faults will belong to a equipment parent. 
#     There can be many faults to one equipment"""

#     def get_equipment(self):
#         return self.equipment

#     def __str__(self):
#         return self.name



    

# # not sure if we need this
# class DefectFault(models.Model):
#     """Model to represent a reported defect fault."""
#     equipment = models.ForeignKey(Equipment, null=True, on_delete=models.SET_NULL)
#     fault = models.ForeignKey(EquipmentFault, null=True, on_delete=models.SET_NULL)
    
#     def __str__(self):
#         return self.fault


class Defect(models.Model):
    """Model to represent a reported defect."""
    creation_datetime = models.DateTimeField(auto_now_add=True)
    registration = models.CharField(max_length=20, db_index=True)
    user = models.ForeignKey(DataliveUser, null=True, on_delete=models.SET_NULL)
    depot = models.ForeignKey(VehicleGroup, null=True, on_delete=models.SET_NULL)
    #faults = models.ManyToManyField(EquipmentFault)
    # faults = models.ManyToManyField(DefectFault)
    defect_faults = models.ManyToManyField(EquipmentResponse)
    defect_photo = models.ImageField(upload_to='defects/photos/%Y/%m/%d', blank=True, null=True)
    #models.URLField(blank=True, null=True) 
    other_details = models.TextField(max_length=255, blank=True, null=True)
    sent_datetime = models.DateTimeField(null=True, blank=True)
    """ Date and time from mobile app when submitted """
    def __str__(self):
        return self.registration
