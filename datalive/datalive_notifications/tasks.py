from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.template.loader import get_template

from datalive_vehicle_check.models import Damage, Report
from datalive_cust_veh.models import Region, VehicleGroup, Vehicle
from services.email_service import EmailService
from .models import Notification


# Daily Vehicle Check Damage email - sent to Region contacts and Depot contacts
# and save a notification to datalive_notifications model
def daily_vehicle_check_damage_email(date=timezone.now().date()):
    damages_qs = Damage.objects.filter(date=date)
    regions_ids = {
        # key: region_id
        # value: list of damage_id
    }
    vehicle_groups_ids = {
        # key: vehicle_group_id
        # value: list of damage_id
    }
    sent_emails = []

    # get lists of related regions and vehicle groups
    for obj in damages_qs.values('vehicle__vehiclegroup__region', 'vehicle__vehiclegroup', 'pk'):
        if obj['vehicle__vehiclegroup__region']:
            if obj['vehicle__vehiclegroup__region'] in regions_ids:
                regions_ids[obj['vehicle__vehiclegroup__region']].append(obj['pk'])
            else:
                regions_ids[obj['vehicle__vehiclegroup__region']] = [obj['pk']]
        if obj['vehicle__vehiclegroup']:
            if obj['vehicle__vehiclegroup'] in vehicle_groups_ids:
                vehicle_groups_ids[obj['vehicle__vehiclegroup']].append(obj['pk'])
            else:
                vehicle_groups_ids[obj['vehicle__vehiclegroup']] = [obj['pk']]

    # send email for each region
    for region in Region.objects.filter(pk__in=regions_ids.keys()).prefetch_related('notifications_emails'):
        # get damages and vehicles related with this region
        damages = damages_qs.filter(pk__in=regions_ids.get(region.pk, []))
        region_vehicles_ids = set(region.VehicleGroups.values_list('vehicles__id', flat=True))
        num_checked_vehicles = Report.objects.filter(vehicle__in=region_vehicles_ids, date=date).distinct().count()

        # render text and html body for email
        context = {
            'region_name': region.name,
            'report_date': date.strftime('%d/%m/%Y'),
            'num_checked': num_checked_vehicles,
            'num_unchecked': len(region_vehicles_ids) - num_checked_vehicles,
            'new_damages': damages.filter(status='NEW').count(),
            'unfixed_damages': Damage.objects.exclude(status='FIX').filter(vehicle__in=region_vehicles_ids).count(),
            'dashboard_url': '',
        }
        text_content = get_template('notifications/emails/daily_vehicle_check_damage_email_region.txt').render(context)
        html_content = get_template('notifications/emails/daily_vehicle_check_damage_email_region.html').render(context)

        # send emails to Notifiacation Emails of this region
        for email in region.notifications_emails.filter(email__isnull=False).values_list('email', flat=True).distinct():
            sent_emails.append(email)
            EmailService().send_generic_email(email, 'Vehicle Check Daily Depot summary', text_content, html_content)
            Notification.objects.create(
                notified_by='Automatically Cron msg',
                source='CRON',
                type=Notification.NOTIFICATION_TYPE_DAILY_VEHICLE_CHECK_EMAIL,
                text=text_content,
            )

    # send email to each Vehicle Group
    for vehicle_group in VehicleGroup.objects.filter(pk__in=vehicle_groups_ids.keys()).prefetch_related('notifications_emails'):
        # get damages and vehicles related with this vehicle group
        damages = damages_qs.filter(pk__in=vehicle_groups_ids.get(vehicle_group.pk, []))
        depot_vehicles_ids = set(vehicle_group.vehicles.values_list('id', flat=True))
        num_checked_vehicles = Report.objects.filter(vehicle__in=depot_vehicles_ids, date=date).distinct().count()

        # render text and html body for email
        context = {
            'depot_name': vehicle_group.name,
            'report_date': date.strftime('%d/%m/%Y'),
            'num_checked': num_checked_vehicles,
            'num_unchecked': len(depot_vehicles_ids) - num_checked_vehicles,
            'new_damages': damages.filter(status='NEW').count(),
            'unfixed_damages': Damage.objects.exclude(status='FIX').filter(vehicle__in=depot_vehicles_ids).count(),
            'dashboard_url': '',
        }
        text_content = get_template('notifications/emails/daily_vehicle_check_damage_email_depot.txt').render(context)
        html_content = get_template('notifications/emails/daily_vehicle_check_damage_email_depot.html').render(context)

        # send emails to Notifiacation Emails of this vehicle group
        for email in vehicle_group.notifications_emails.filter(email__isnull=False).values_list('email', flat=True).distinct():
            # prevent duplicate of email if Region report already was sent to this email
            if email not in sent_emails:
                EmailService().send_generic_email(email, 'Vehicle Check Daily Region summary', text_content, html_content)
                Notification.objects.create(
                    notified_by='Automatically Cron msg',
                    source='CRON',
                    type=Notification.NOTIFICATION_TYPE_DAILY_VEHICLE_CHECK_EMAIL,
                    text=text_content,
                )


# MOT Expiry email notifications - send an email
# and save a notification to datalive_notifications model
def mot_expiry_email_notifications():
    # mot expired after 7 days
    vehicles_qs = Vehicle.objects.filter(
        mot_date__lte=timezone.now().date()+timedelta(days=settings.SEND_NOTIFICATION_IF_MOT_EXPIRY_DATE_LESS_THAN_DAYS))
    regions_ids = {
        # key: region_id
        # value: list of vehicle_id
    }
    vehicle_groups_ids = {
        # key: vehicle_group_id
        # value: list of vehicle_id
    }
    sent_emails = []

    # get lists of related regions and vehicle groups
    for obj in vehicles_qs.values('vehiclegroup__region', 'vehiclegroup', 'pk'):
        if obj['vehiclegroup__region']:
            if obj['vehiclegroup__region'] in regions_ids:
                regions_ids[obj['vehiclegroup__region']].append(obj['pk'])
            else:
                regions_ids[obj['vehiclegroup__region']] = [obj['pk']]
        if obj['vehiclegroup']:
            if obj['vehiclegroup'] in vehicle_groups_ids:
                vehicle_groups_ids[obj['vehiclegroup']].append(obj['pk'])
            else:
                vehicle_groups_ids[obj['vehiclegroup']] = [obj['pk']]

    # send email for each region
    for region in Region.objects.filter(pk__in=regions_ids.keys()).prefetch_related('notifications_emails'):
        # get vehicles related with this region
        vehicles = vehicles_qs.filter(pk__in=regions_ids.get(region.pk, []))

        # render text and html body for email
        context = {
            'region_name': region.name,
            'report_date': timezone.now().date().strftime('%d/%m/%Y'),
            'vehicles': vehicles,
        }
        text_content = get_template('notifications/emails/mot_expiry_email_notification_region.txt').render(context)
        html_content = get_template('notifications/emails/mot_expiry_email_notification_region.html').render(context)

        # send emails to Notifiacation Emails of this region
        for email in region.notifications_emails.filter(email__isnull=False).values_list('email', flat=True).distinct():
            sent_emails.append(email)
            EmailService().send_generic_email(email, 'MOT Expiry notification', text_content, html_content)
            Notification.objects.create(
                notified_by='Automatically Cron msg',
                source='CRON',
                type=Notification.NOTIFICATION_TYPE_MOT_EXPIRY_EMAIL,
                text=text_content,
            )

    # send email to each Vehicle Group
    for vehicle_group in VehicleGroup.objects.filter(pk__in=vehicle_groups_ids.keys()).prefetch_related('notifications_emails'):
        # get vehicles related with this vehicle group
        vehicles = vehicles_qs.filter(pk__in=vehicle_groups_ids.get(vehicle_group.pk, []))

        # render text and html body for email
        context = {
            'depot_name': vehicle_group.name,
            'report_date': timezone.now().date().strftime('%d/%m/%Y'),
            'vehicles': vehicles,
        }
        text_content = get_template('notifications/emails/mot_expiry_email_notification_depot.txt').render(context)
        html_content = get_template('notifications/emails/mot_expiry_email_notification_depot.html').render(context)

        # send emails to Notifiacation Emails of this vehicle group
        for email in vehicle_group.notifications_emails.filter(email__isnull=False).values_list('email', flat=True).distinct():
            # prevent duplicate of email if Region report already was sent to this email
            if email not in sent_emails:
                EmailService().send_generic_email(email, 'MOT Expiry notification', text_content, html_content)
                Notification.objects.create(
                    notified_by='Automatically Cron msg',
                    source='CRON',
                    type=Notification.NOTIFICATION_TYPE_MOT_EXPIRY_EMAIL,
                    text=text_content,
                )
