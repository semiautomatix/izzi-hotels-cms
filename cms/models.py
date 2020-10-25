from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
# import the logging library
import logging
from django.core.validators import MaxValueValidator, MinValueValidator

# email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

# Get an instance of a logger
logger = logging.getLogger('django')

class Hotel(models.Model):

    #  Relationships 
    hotel_group = models.ForeignKey("cms.HotelGroup", on_delete=models.CASCADE)

    #  Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    # geolocation = models.CharField(max_length=100)
    longitude = models.DecimalField(default=0.00, max_digits=10, decimal_places=7)
    latitude = models.DecimalField(default=0.00, max_digits=10, decimal_places=7)    
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    hotel_name = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    address = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="upload/images/")
    contact_number = models.CharField(max_length=40, null=True, blank=True)
    short_description = models.CharField(max_length=40, null=True, blank=True)
    long_description = models.CharField(max_length=1000, null=True, blank=True)
    ibe_domain = models.CharField(max_length=100, null=True, verbose_name="IBE Domain")
    ibe_id = models.IntegerField(null=True, verbose_name="IBE Id")

    class Meta:
        pass 
    
    def __str__(self):
        return str(self.hotel_name)  

    def get_absolute_url(self):
        return reverse("cms_Hotel_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("cms_Hotel_update", args=(self.pk,))


class Room(models.Model):

    #  Relationships
    hotel = models.ForeignKey("cms.Hotel", on_delete=models.CASCADE)

    #  Fields
    room_number = models.CharField(max_length=10)
    max_persons = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(20)])
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("cms_Room_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("cms_Room_update", args=(self.pk,))    


class Booking(models.Model):

    #  Relationships
    hotel_group = models.ForeignKey("cms.HotelGroup", on_delete=models.CASCADE)
    hotel = models.ForeignKey("cms.Hotel", on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    room = models.ForeignKey("cms.Room", on_delete=models.CASCADE, blank=True, null=True)    

    #  Fields
    end_date = models.DateField()
    adults = models.IntegerField(default=1,validators=[MinValueValidator(1)])
    start_date = models.DateField()
    booking_status = models.TextField(max_length=100, choices=(('0','Cancelled'),('1','Confirmed'),('2','Checked In'),('3','Checked Out')))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    children = models.PositiveIntegerField(default=0)
    rooms =  models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    check_out_date_time = models.DateTimeField(null=True) # time of checking in, meetings only
    check_in_date_time = models.DateTimeField(null=True) #  time of checking out, meetings only


    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("cms_Booking_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("cms_Booking_update", args=(self.pk,))

    # define under save will apply to both app and CMS
    def save(self, force_insert=False, force_update=False, using=None,
        update_fields=None):
        if not self.id: #if creating
            self.booking_status = 1
            user = self.user

            # send booking email
            msg_plain = render_to_string('email/booking_confirmation.txt', { 'user': user, 'booking': self, 'site_name': Site.objects.get_current().domain })
            msg_html = render_to_string('email/booking_confirmation.html', { 'user': user, 'booking': self,  'site_name': Site.objects.get_current().domain })

            send_mail(
                'Booking confirmation',
                msg_plain,
                settings.FROM_EMAIL_ADDRESS,
                recipient_list=[user.email],
                html_message=msg_html,
            )               

        return super(Booking, self).save()                  


class Icon(models.Model):

    #  Fields 
    image = models.ImageField(upload_to="upload/images/")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    icon_name = models.CharField(max_length=100, blank=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.icon_name) 

    def get_absolute_url(self):
        return reverse("cms_ServiceCategory_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("cms_ServiceCategory_update", args=(self.pk,))


class ServiceCategory(models.Model):
    # Fields
    category_name = models.CharField(max_length=50, blank=True)
    hotel = models.ForeignKey("cms.Hotel", on_delete=models.CASCADE, null=True, blank=True)
    hotel_group = models.ForeignKey("cms.HotelGroup", on_delete=models.CASCADE, null=True, blank=True)
    icon = models.ForeignKey("cms.Icon", on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)    

    class Meta:
        pass
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return str(self.category_name)

    def get_absolute_url(self):
        return reverse("cms_Service_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("cms_Service_update", args=(self.pk,))    


class Service(models.Model):

    #  Relationships
    hotel = models.ForeignKey("cms.Hotel", on_delete=models.CASCADE, null=True, blank=True)
    hotel_group = models.ForeignKey("cms.HotelGroup", on_delete=models.CASCADE, null=True, blank=True)
    icon = models.ForeignKey("cms.Icon", on_delete=models.CASCADE)
    # ON DELETE Set existing services categories to NULL (For the services to belisted on the app they must be assigned to a category).
    service_category = models.ForeignKey("cms.ServiceCategory", null=True, blank=True, on_delete=models.SET_NULL) 

    #  Fields
    service_name = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    meeting_room = models.CharField(max_length=50, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    service_type = models.CharField(max_length=20, choices=(('service','Service'),('co_share','Co-share'),('meeting_room','Meeting Room')),default='service')
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        pass

    def __str__(self):
        return str(self.service_name)

    def get_absolute_url(self):
        return reverse("cms_Service_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("cms_Service_update", args=(self.pk,))

    def clean(self):
        # validation fields based on service type
        if self.service_type == 'service': 
            validation_errors = {}
            if not self.service_name:
                validation_errors['service_name'] = ["This field is required.",] 
            #if not self.service_category:
            #    validation_errors['service_category'] = ["This field is required.",] 
            raise ValidationError(validation_errors)
        elif self.service_type == 'meeting_room': 
            validation_errors = {}
            if not self.hotel_group:
                validation_errors['hotel_group'] = ["This field is required.",] 
            if not self.hotel:
                validation_errors['hotel'] = ["This field is required.",] 
            if not self.location:
                validation_errors['location'] = ["This field is required.",] 
            if not self.meeting_room:
                validation_errors['meeting_room'] = ["This field is required.",] 
            raise ValidationError(validation_errors)
        else:
            validation_errors = {}
            if not self.hotel_group:
                validation_errors['hotel_group'] = ["This field is required.",] 
            if not self.hotel:
                validation_errors['hotel'] = ["This field is required.",] 
            if not self.hotel:
                validation_errors['location'] = ["This field is required.",] 
            raise ValidationError(validation_errors)


class HotelGroup(models.Model):

    #  Fields
    hotel_group_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="upload/images/")
    head_office_address = models.CharField(max_length=100)
    head_office_postal_code = models.CharField(max_length=10)
    head_office_city = models.CharField(max_length=40)
    head_office_country = models.CharField(max_length=40)
    # head_office_geolocation = models.CharField(max_length=100, blank=True)
    head_office_latitude = models.DecimalField(default=0.00, max_digits=10, decimal_places=7, blank=True)
    head_office_longitude = models.DecimalField(default=0.00, max_digits=10, decimal_places=7, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.hotel_group_name)  

    def get_absolute_url(self):
        return reverse("cms_HotelGroup_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("cms_HotelGroup_update", args=(self.pk,))


class HotelGallery(models.Model):

    # Relationships
    # rating = models.ForeignKey("mobile.Rating", null=True, on_delete=models.SET_NULL)
    hotel = models.ForeignKey("cms.Hotel", on_delete=models.CASCADE)

    #  Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField(upload_to="upload/images/")
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("cms_HotelGallery_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("cms_HotelGallery_update", args=(self.pk,))


class Subscription(models.Model):

    #  Fields 
    subscription_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subscription_unit = models.CharField(max_length=20, choices=(('hour','Per hour'),('day','Per day'),('week','Per week'),('month','Per month')), default='hour', unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.subscription_unit) 

    def get_absolute_url(self):
        return reverse("cms_Subscription_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("cms_Subscription_update", args=(self.pk,))


class Subscriber(models.Model):

    #  Fields 
    subscription = models.ForeignKey("cms.Subscription", on_delete=models.CASCADE)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.user) 

    def get_absolute_url(self):
        return reverse("cms_Subscriber_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("cms_Subscriber_update", args=(self.pk,)) 


@receiver(pre_save, sender=Subscription)
def user_metadata_updated(sender, **kwargs):
    subscription = kwargs.get('instance', None)
    old_subscription = Subscription.objects.get(pk=subscription.pk)
    if subscription:
        #Sends an email of subscription rate changes    
        if subscription.rate != old_subscription.rate:
            context = {
                'site_name': Site.objects.get_current().domain,
                'subscription': subscription
            }

            msg_plain = render_to_string('email/subscription_change.txt', context)
            msg_html = render_to_string('email/subscription_change.html', context)

            receivers = Subscriber.objects.get(subscription_id=subscription.pk).filter(user__is_active=True).values_list('user__email', flat=True)        

            send_mail(
                'Subscription changes',
                msg_plain,
                settings.FROM_EMAIL_ADDRESS,
                [receivers],
                html_message=msg_html,
            )

class File(models.Model):
    file = models.FileField(upload_to='upload/images/', blank=False, null=False)
    def __str__(self):
        return self.file.name            