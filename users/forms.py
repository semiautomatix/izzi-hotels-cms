from django import forms
from django.conf import settings
from . import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm
from users.models import UserMetadata
from django.contrib.auth.models import User

# email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

# import the logging library
import logging


# Get an instance of a logger
logger = logging.getLogger('django')
logger.info("logger initalized " + __name__ + " forms.py")


class UserMetadataForm(forms.ModelForm):
    class Meta:
        model = models.UserMetadata
        fields = [
            "age_range",
            "profile_picture",
            "middle_name",
            "profile_picture",
            "nationality",
            "position",
            "gender",
            "user",
            "hotel",
            "hotel_group",
        ]  

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=None,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):

        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email_address = self.cleaned_data["email"]

        try:
            user_instance = User.objects.get(email=email_address)
            one_time_password = User.objects.make_random_password()
            user_instance.set_password(one_time_password)
            user_instance.save()

            try:
                user_metadata_instance = UserMetadata.objects.get(user_id=user_instance.id) 
                user_metadata_instance.change_password = True

                msg_plain = render_to_string('email/forgot_password.txt', { 'user': user_instance, 'password': one_time_password, 'site_name': Site.objects.get_current().domain })
                msg_html = render_to_string('email/forgot_password.html', { 'user': user_instance, 'password': one_time_password, 'site_name': Site.objects.get_current().domain })

                send_mail(
                    'Password reset',
                    msg_plain,                    
                    settings.FROM_EMAIL_ADDRESS,
                    recipient_list=[user_instance.email],
                    html_message=msg_html,
                )

            except User.DoesNotExist: 
                return

        except User.DoesNotExist: 
            return