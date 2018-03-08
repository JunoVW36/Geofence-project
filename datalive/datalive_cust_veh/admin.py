# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from .models import *



class InsuranceAdmin(admin.ModelAdmin):
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }
    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL', 'static') 
        # js = ('https://cdn.ckeditor.com/ckeditor5/1.0.0-alpha.2/classic/ckeditor.js', )
        js = ('https://cdn.ckeditor.com/ckeditor5/1.0.0-alpha.2/classic/ckeditor.js', 
        'admin/js/custom/textarea.js',)



class FAQDescriptionInline(admin.TabularInline):
    model = FAQDescription
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }
    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL', 'static') 
        # js = ('https://cdn.ckeditor.com/ckeditor5/1.0.0-alpha.2/classic/ckeditor.js', )
        js = ('https://cdn.ckeditor.com/ckeditor5/1.0.0-alpha.2/classic/ckeditor.js', 
        'admin/js/custom/textarea.js',)



class FAQAdmin(admin.ModelAdmin):
    inlines = [
        FAQDescriptionInline,
    ]

class FAQDescriptionAdmin(admin.ModelAdmin):
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }

class LiveryAdmin(admin.ModelAdmin):
    filter_horizontal = ('views', )


class VehicleGroupAdmin(admin.ModelAdmin):
     filter_horizontal = ('vehicles', 'vehicle_group_contacts', 'notifications_emails')

admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(InsurancePolicyNumber)
admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(VehicleManufacturer)
admin.site.register(VehicleManufacturerModel)
admin.site.register(LiverySchematic)
# admin.site.register(VehicleSchematic)
admin.site.register(SchematicView)
admin.site.register(DriverCategory)
admin.site.register(VehicleTracker)
admin.site.register(Region)
admin.site.register(VehicleGroup, VehicleGroupAdmin)
admin.site.register(VehicleGroupContact)

admin.site.register(FAQ, FAQAdmin)
admin.site.register(FAQDescription, FAQDescriptionAdmin)
admin.site.register(FAQActions)
admin.site.register(NotificationEmail)
admin.site.register(LeaseCompany)



# class InsuranceAdmin(admin.ModelAdmin):
#     change_form_template = 'fun/admin/change_form.html'

# admin.site.register(Playground, PlaygroundAdmin)
