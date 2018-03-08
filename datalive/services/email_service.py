from django.conf import settings

from django.template.loader import get_template
from google.appengine.api import mail



class EmailService(object):

    def send_reset_password_email(self, user, token):
        url = settings.SITE_URL + '/reset_password_key?token=' + token
        context = {
            'user': user,
            'token': token,
            'url': url,
            'site_url': settings.SITE_URL,
        }

        html_content = get_template('emails/reset-password-email.html').render(context)
        
        message = mail.EmailMessage(sender=settings.NOTIFICATIONS_EMAIL_ADDRESS,
                                    subject='Datalive - Reset password for ' + user.first_name)

        message.to = user.email
        message.body = "Please open the following link to login initially or to reset your password: %s " % (url)
        message.html = html_content
        # message.html = '<html><head></head><body><div>' \
        #                     '<p><span>Please click link below to login: </span>' \
        #                     '<a href="%s">click here</a></p><p>&nbsp;</p>' \
        #                '</div></body></html>' % (url)

        message.send()

    def send_welcome_password_email(self, user, token):
        url = settings.SITE_URL + '/set_password?token=' + token
        # render text and html body for email
        context = {
            'user': user,
            'token': token,
            'url': url,
            'site_url': settings.SITE_URL,
        }
        text_content = get_template('notifications/emails/daily_vehicle_check_damage_email_region.txt').render(context)
        html_content = get_template('emails/welcome-email.html').render(context)


        message = mail.EmailMessage(sender=settings.NOTIFICATIONS_EMAIL_ADDRESS,
                                    subject='Welcome to Datalive, ' + user.first_name)
       

        message.to = user.email
        message.body = "Please open the following link to complete registration: %s " % (url)
        message.html = html_content
        # '<html><head></head><body><div>' \
        #                '<h3>Welcome on Datalive! </h3>' \
        #                '<p><span>Please <a href="%s">click here</a> to complete registration </span></p>' \
        #                '</div></body></html>' % (url)

        message.send()

    
    def send_defect_notification_email(self, user, defect):
        message = mail.EmailMessage(sender=settings.NOTIFICATIONS_EMAIL_ADDRESS,
                                    subject='Welcome to Datalive!' + user.first_name)
                             
        message.to = settings.DEFECT_CONFIRMATION_EMAIL
        message.body = "A new defect has been submitted: '{0}' ".format(defect)
        message.html = '<html><head></head><body><div>' \
                       '<h3>A new defect has been submitted: </h3>' \
                       'Submitted by:' \
                       '<p><span> {0} </span></p>' \
                       '</div></body></html>'.format(defect)

        message.send()
    
    def send_generic_email(self, to_address, email_subject, email_body, email_html=None):
        """ Generic send email method """

        message = mail.EmailMessage(sender=settings.NOTIFICATIONS_EMAIL_ADDRESS,
                                    subject=email_subject)
                             
        message.to = to_address
        message.body = email_body

        if email_html:
            message.html = email_html

        message.send()
