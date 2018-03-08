# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *


class ReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'type', 'report_class', 'vehicle', 'checker_name')


class GateCheckReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'hub', 'depot', 'driver_name')


class QuestionDefinitionAdmin(admin.ModelAdmin):
    list_display = ('description', 'type')


class AuditSurveyTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'created_by')


class AuditSurveyReportAdmin(admin.ModelAdmin):
    list_display = ('depot', 'created_by', 'added')


admin.site.register(Damage)
admin.site.register(Report, ReportAdmin)
admin.site.register(QuestionDefinitionAnswer)
admin.site.register(QuestionDefinition, QuestionDefinitionAdmin)
admin.site.register(QuestionResponse)
admin.site.register(GateCheckReport, GateCheckReportAdmin)
admin.site.register(AuditSurveyReport, AuditSurveyReportAdmin)
admin.site.register(AuditSurveyTemplate, AuditSurveyTemplateAdmin)
