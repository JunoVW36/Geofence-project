# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
#DefectSetting, Defect, EquipmentDefinition, EquipmentDefinitionFault, EquipmentResponse
# Register your models here.

# class StepInline(admin.TabularInline):
#     model = EquipmentDefinitionFault

# class EquipmentAdmin(admin.ModelAdmin):
#     inlines = [StepInline,]

admin.site.register(Defect)
#admin.site.register(DefectFault)
#admin.site.register(Equipment, EquipmentAdmin)
#admin.site.register(EquipmentFault)
admin.site.register(EquipmentDefinitionFault)
admin.site.register(EquipmentDefinition)
admin.site.register(EquipmentResponse)
