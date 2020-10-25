from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from allauth.account.signals import password_changed
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.contrib import messages
from social_django.models import UserSocialAuth

# email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

User._meta.get_field('email').blank = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('last_name').blank = False

@receiver(pre_save, sender=User)
def user_updated(sender, **kwargs):
    user = kwargs.get('instance', None)
    try:
        old_user = User.objects.get(pk=user.pk)

        # only if not a Social Auth user
        try:
            UserSocialAuth.objects.get(user_id=user.pk)
        except UserSocialAuth.DoesNotExist:
            user.email = user.username
        new_password = user.password
        try:
            old_password = old_user.password       
        except User.DoesNotExist:
            old_password = None
        if new_password != old_password:    
            # update user meta data to state user has changed password
            # if user was forced to change password previously, this is unset
            try:
                user_metadata = UserMetadata.objects.get(user_id=user.pk)
                user_metadata.change_password = False
                user_metadata.save()
            except UserMetadata.DoesNotExist:
                return  
        
        if user.is_staff: 
            # if a backend user send update email
            context = {
                'user': user, 
                'site_name': Site.objects.get_current().domain
            }

            changed = False

            if new_password != old_password:
                context['password'] = user.pk
                changed = True
            if user.email != old_user.email:
                context['email'] = user.email
                changed = True

                # also required to delete all sessions
                user.session_set.filter(user_id=user.pk).delete()
            if user.first_name != old_user.first_name:
                context['first_name'] = user.first_name
                changed = True
            if user.last_name != old_user.last_name:
                context['last_name'] = user.last_name
                changed = True
            
            if changed:
                msg_plain = render_to_string('email/user_changed.txt', context)
                msg_html = render_to_string('email/user_changed.html', context)

                send_mail(
                    'User details changes',
                    msg_plain,
                    settings.FROM_EMAIL_ADDRESS,
                    recipient_list=[user.email],
                    html_message=msg_html,
                )   
    # ignore, as most likely a new user
    except User.DoesNotExist:
        return         

@receiver(post_delete, sender=User)
def user_delete(sender, **kwargs):
    user = kwargs.get('instance', None)
    if user:
        msg_plain = render_to_string('email/user_deleted.txt', { 'user': user, 'site_name': Site.objects.get_current().domain })
        msg_html = render_to_string('email/user_deleted.html', { 'user': user, 'site_name': Site.objects.get_current().domain })

        send_mail(
            'Account deleted',
            msg_plain,
            settings.FROM_EMAIL_ADDRESS,
            recipient_list=[user.email],
            html_message=msg_html,
        )                                                 

class UserMetadata(models.Model):

    #  Relationships
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    hotel = models.ForeignKey("cms.Hotel", on_delete=models.CASCADE, blank=True, null=True)
    hotel_group = models.ForeignKey("cms.HotelGroup", on_delete=models.CASCADE, blank=True, null=True)

    #  Fields
    # user_type = models.CharField(max_length=20, choices=(('global','Global Administrator'),('group', 'Hotel Group Administrator'),('hotel','Hotel Administrator'),('user','End User'),), default='user')
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=(('male','Male'),('female','Female'),('non_binary','Non binary')), blank=True, null=True)
    age_range = models.CharField(max_length=20,choices=(('18','18-24'),('25','25-34'),('35','35-44'),('45','45-54'),('55','55-64'),('65','65+')), blank=True, null=True)
    nationality = models.CharField(max_length=50,blank=True, null=True)
    position = models.CharField(max_length=50,blank=True, null=True)
    profile_picture = models.ImageField(upload_to="upload/images/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    uid = models.CharField(max_length=28,blank=True, null=True, unique=True) # firebase UID
    change_password = models.BooleanField(default=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("users_UserMetadata_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("users_UserMetadata_update", args=(self.pk,))

@receiver(pre_save, sender=UserMetadata)
def user_metadata_updated(sender, **kwargs):
    user_metadata = kwargs.get('instance', None)   
    if user_metadata and user_metadata.pk:
        try:            
            old_user_metadata = UserMetadata.objects.get(pk=user_metadata.pk)
            user = User.objects.get(pk=user_metadata.user_id)
            if user.is_staff: 
                # if a backend user send update email
                context = {
                    'user': user, 
                    'site_name': Site.objects.get_current().domain
                }
                changed = False
                if user_metadata.profile_picture != old_user_metadata.profile_picture:
                    context['profile_picture'] = old_user_metadata.profile_picture
                    changed = True
                if user_metadata.position != old_user_metadata.position:
                    context['position'] = old_user_metadata.position
                    changed = True
                if user_metadata.gender != old_user_metadata.gender:
                    context['gender'] = old_user_metadata.gender
                    changed = True
                if changed:
                    msg_plain = render_to_string('email/user_metadata_changed.txt', context)
                    msg_html = render_to_string('email/user_metadata_changed.html', context)

                    send_mail(
                        'User details changes',
                        msg_plain,
                        settings.FROM_EMAIL_ADDRESS,
                        recipient_list=[user.email],
                        html_message=msg_html,
                    )
        except UserMetaData.DoesNotExist:
            # a new user, so no need to send changed email
            None 

