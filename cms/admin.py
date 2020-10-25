from django.conf import settings
from django.contrib import admin, messages
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.contrib.auth.models import User
import datetime
# import the logging library
import logging

from users.models import UserMetadata
from mobile.models import Rating
from . import models
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
import itertools
from django.utils.html import format_html

# email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


# Get an instance of a logger
logger = logging.getLogger('django')

class HotelAdminForm(forms.ModelForm):

    class Meta:
        model = models.Hotel
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        # get current user
        current_user = self.request.user   
        super(HotelAdminForm, self).__init__(*args, **kwargs)        
        self.fields['city'].widget.attrs.update({'readonly':''})
        self.fields['country'].widget.attrs.update({'readonly':''})
        self.fields['postal_code'].widget.attrs.update({'readonly':''})
        # self.fields['geolocation'].widget.attrs.update({'readonly':''})        
        self.fields['latitude'].widget.attrs.update({'readonly':''})        
        self.fields['longitude'].widget.attrs.update({'readonly':''})        
        # fitler the select lists based on user groups 
        try:
            # get metadata for current user    
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists() | current_user.groups.filter(name='Hotel Administrators').exists():                
                hotel_group_id = user_metadata.hotel_group_id
                # filter hotel choices based on group   
                hotel_groups = models.HotelGroup.objects.filter(id=hotel_group_id)
                choices = ((x.id, x.hotel_group_name) for x in hotel_groups)
                self.fields['hotel_group'].widget.choices = choices
        except UserMetadata.DoesNotExist:     
            None  

class HotelGalleryInline(admin.TabularInline):
    model = models.HotelGallery

class HotelRatingInline(admin.TabularInline):
    model = Rating

class HotelRoomInline(admin.TabularInline):
    model = models.Room

class HotelAdmin(admin.ModelAdmin):
    form = HotelAdminForm
    def get_form(self, request, obj=None, **kwargs):
        form = super(HotelAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form       
    list_display = [
        "hotel_name",
        "hotel_group",
        "address",
        "postal_code",
        "city",
        "country",
        # "geolocation",
        "created",
        "last_updated",
    ]
    readonly_fields = [       
        "created",
        "last_updated",
    ]
    fields = [
        "hotel_name",
        "hotel_group",
        "address",
        "postal_code",
        "city",
        "country",
        "contact_number",
        # "geolocation",
        "latitude",
        "longitude",
        "short_description",
        "long_description",
        "ibe_domain",
        "ibe_id",
    ]
    search_fields = [
        'hotel_name',
        'hotel_group__hotel_group_name',
        'city',
        'country'
    ]   
    list_filter = [
        'hotel_group',
    ]       
    inlines = [        
        HotelGalleryInline,
        HotelRatingInline,
        HotelRoomInline,     
    ]
    def get_queryset(self, request):
        qs = super(HotelAdmin, self).get_queryset(request)  
        # get current user
        current_user = request.user    
        # get metadata for current user
        try:
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists():
                hotel_group_id = user_metadata.hotel_group_id
                return qs.filter(hotel_group_id=hotel_group_id)
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                hotel_id = user_metadata.hotel_id
                return qs.filter(id=hotel_id)
            return qs
        except UserMetadata.DoesNotExist:     
            return models.Hotel.objects.all()  # Global admin might not have usermetadata
        return models.Hotel.objects.all()

class RoomAdminForm(forms.ModelForm):

    class Meta:
        model = models.Room
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        # get current user
        current_user = self.request.user   
        super(RoomAdminForm, self).__init__(*args, **kwargs)        
        # get metadata for current user    
        # fitler the select lists based on user groups 
        try:
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists():                
                hotel_group_id = user_metadata.hotel_group_id
                # filter hotel choices based on group   
                hotels = models.Hotel.objects.filter(hotel_group_id=hotel_group_id)
                choices = ((x.id, x.hotel_name) for x in hotels)
                self.fields['hotel'].widget.choices = choices
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                hotel_id = user_metadata.hotel_id
                # filter hotel choices
                hotels = models.Hotel.objects.filter(id=hotel_id)
                choices = ((x.id, x.hotel_name) for x in hotels)
                self.fields['hotel'].widget.choices = choices
        except UserMetadata.DoesNotExist:     
            None     


class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    # add the request to the form
    def get_form(self, request, obj=None, **kwargs):
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form         
    list_display = [
        "room_number",
        "hotel",
        "last_updated",
        "created",
    ]
    search_fields = [
        'room_number',
        'hotel__hotel_name'
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]
    def get_queryset(self, request):
        qs = super(RoomAdmin, self).get_queryset(request)  
        # get current user
        current_user = request.user    
        # get metadata for current user
        # filter list based on user groups
        try:
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists():                
                hotel_group_id = user_metadata.hotel_group_id
                # filter hotel choices
                # need to filter where a hotel's group id is hotel_group_id
                return qs.filter(hotel_group_id=hotel_group_id)
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                hotel_id = user_metadata.hotel_id
                # filter hotel choices
                return qs.filter(hotel_id=hotel_id)
            return qs
        except UserMetadata.DoesNotExist:     
            return models.Room.objects.all()  # Global admin might not have usermetadata
        return models.Room.objects.all()   # Global admin might not have usermetadata  


class BookingAdminForm(forms.ModelForm):

    class Meta:
        model = models.Booking
        fields = '__all__'   
    def __init__(self, *args, **kwargs):
        # changing drop down filter to ajax
        current_user = self.request.user

        super(BookingAdminForm, self).__init__(*args, **kwargs)              

        # get metadata for current user    
        # fitler the select lists based on user groups 
        try:
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel            
            # if adding a booking set hotel and room to null
            if not self.instance.id:            
                self.fields['hotel'].widget.choices = []
                self.fields['room'].widget.choices = [] 
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists():                
                hotel_group_id = user_metadata.hotel_group_id

                # filter hotel group choices based on group   
                hotel_groups = models.HotelGroup.objects.filter(id=hotel_group_id)
                choices = ((x.id, x.hotel_group_name) for x in hotel_groups)
                self.fields['hotel_group'].widget.choices = choices                

                # filter hotel choices based on group   
                hotels = models.Hotel.objects.filter(hotel_group_id=hotel_group_id)
                choices = ((x.id, x.hotel_name) for x in hotels)
                self.fields['hotel'].widget.choices = choices

                if self.instance.id: # if editing record
                    hotel_id = self.instance.hotel_id
                    # filter room choices based on group 
                    rooms = models.Room.objects.filter(hotel_id=hotel_id)
                    choices = ((x.id, x.room_number) for x in rooms)
                    self.fields['room'].widget.choices = choices  
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                hotel_id = user_metadata.hotel_id

                # filter hotel choices based on group 
                hotels = models.Hotel.objects.filter(id=hotel_id)
                choices = ((x.id, x.hotel_name) for x in hotels)
                self.fields['hotel'].widget.choices = choices

                # filter room choices based on group 
                rooms = models.Room.objects.filter(hotel_id=hotel_id)
                choices = ((x.id, x.room_number) for x in rooms)
                self.fields['room'].widget.choices = choices                
            elif self.instance.id: # filter for global administrators if editing record
                hotel_group_id = self.instance.hotel_group_id
                # filter hotel choices based on group   
                hotels = models.Hotel.objects.filter(hotel_group_id=hotel_group_id)
                choices = ((x.id, x.hotel_name) for x in hotels)
                self.fields['hotel'].widget.choices = choices

                hotel_id = self.instance.hotel_id
                # filter room choices based on group 
                rooms = models.Room.objects.filter(hotel_id=hotel_id)
                choices = ((x.id, x.room_number) for x in rooms)
                self.fields['room'].widget.choices = choices                    

            # only end users, not administrators
            users = User.objects.exclude(groups__name__in=['Hotel Administrators', 'Hotel Group Administrators', 'Global Administrators'])
            choices = ((x.id, x.username) for x in users)
            self.fields['user'].widget.choices = choices        

        except UserMetadata.DoesNotExist:     
            None

    # where validation occurs
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")     
                             

class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm
    # add the request to the form
    def get_form(self, request, obj=None, **kwargs):
        form = super(BookingAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form          
    list_display = [
        "hotel_group",
        "hotel",
        "user",
        "adults",
        "children",
        "start_date",
        "end_date",
        "booking_status",
        "created",
        "last_updated",
    ]
    readonly_fields = [        
        "booking_status",
        "check_in_date_time",
        "check_out_date_time",
        "created",
        "last_updated",
    ]
    fields = [
        "user",
        "hotel_group",
        "hotel",
        "room",  # this needs to be hidden for global and group      
        "start_date",
        "end_date",
        "adults",
        "children",
        "rooms",
        "booking_status",
    ]
    search_fields = [
        "hotel_group__hotel_group_name",
        "hotel__hotel_name",
        "user__username",
        "start_date"
    ] 
    list_filter = [
        'hotel_group',
        'hotel',
        'user',
    ]           
    
    def cancel_bookings(self, request, queryset):
        queryset.update(booking_status=0) # cancelled
        for booking in queryset:
            # send email
            user = booking.user
            if user:
                msg_plain = render_to_string('email/booking_cancellation.txt', { 'user': user, 'booking': booking, 'site_name': Site.objects.get_current().domain })
                msg_html = render_to_string('email/booking_cancellation.html', { 'user': user, 'booking': booking,  'site_name': Site.objects.get_current().domain })

                send_mail(
                    'Booking cancellation',
                    msg_plain,
                    settings.FROM_EMAIL_ADDRESS,
                    recipient_list=[user.email],
                    html_message=msg_html,
                )
    cancel_bookings.short_description = "Cancel selected bookings"     
    actions = ['cancel_bookings']   

    def get_actions(self, request):
        #Disable delete
        actions = super(BookingAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False   

    def response_change(self, request, obj):
        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)
        if "_cancel_booking" in request.POST:
            # handle the action on your obj  
            # defining under admin only applies to CMS
            obj.booking_status = 1 # Cancelled   
            obj.save()   

            # send email
            user = obj.user
            if user:
                msg_plain = render_to_string('email/booking_cancellation.txt', { 'user': user, 'booking': obj, 'site_name': Site.objects.get_current().domain })
                msg_html = render_to_string('email/booking_cancellation.html', { 'user': user, 'booking': obj,  'site_name': Site.objects.get_current().domain })

                send_mail(
                    'Booking cancellation',
                    msg_plain,
                    settings.FROM_EMAIL_ADDRESS,
                    recipient_list=[user.email],
                    html_message=msg_html,
                )
                
            messages.success(request, 'Booking was cancelled')
            redirect_url = reverse('admin:%s_%s_change' %
                               (opts.app_label, opts.model_name),
                               args=(pk_value,),
                               current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)
        else:
             return super(BookingAdmin, self).response_change(request, obj)    

    def get_queryset(self, request):
        qs = super(BookingAdmin, self).get_queryset(request)  
        # get current user
        current_user = request.user    
        # get metadata for current user
        # filter list based on user groups
        try:
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists():                
                hotel_group_id = user_metadata.hotel_group_id
                # filter hotel choices
                # need to filter where a hotel's group id is hotel_group_id
                return qs.filter(hotel_group_id=hotel_group_id)
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                hotel_id = user_metadata.hotel_id
                # filter hotel choices
                return qs.filter(hotel_id=hotel_id)
            return qs
        except UserMetadata.DoesNotExist:     
            return models.Booking.objects.all()  # Global admin might not have usermetadata
        return models.Booking.objects.all()  # Global admin might not have usermetadata                     

class IconAdminForm(forms.ModelForm):

    class Meta:
        model = models.Icon
        fields = "__all__"


class IconAdmin(admin.ModelAdmin):
    form = IconAdminForm
    list_display = [
        "icon_name",
        "image_tag",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-height: 40px"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'


class ServiceCategoryAdminForm(forms.ModelForm):

    class Meta:
        model = models.ServiceCategory
        fields = "__all__"

class ServiceCategoryAdmin(admin.ModelAdmin):
    form = ServiceCategoryAdminForm
    # add the request to the form
    def get_form(self, request, obj=None, **kwargs):
        form = super(ServiceCategoryAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form      
    list_display = [ 
        "id",
        "category_name",
        "hotel_group",
        "hotel",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]
    fields = [
        "icon",
        "category_name",
        "hotel_group",
        "hotel",
        "created",
        "last_updated",
    ]
    search_fields = [
        "hotel_group__hotel_group_name",
        "hotel__hotel_name",
        "category_name" 
    ] 
    list_filter = [
        'hotel_group',
        'hotel'
    ]  

    def get_queryset(self, request):
        qs = super(ServiceCategoryAdmin, self).get_queryset(request)  
        # get current user
        current_user = request.user    
        # get metadata for current user
        # filter list based on user groups
        try:
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists():                
                hotel_group_id = user_metadata.hotel_group_id
                # filter hotel choices
                # need to filter where a hotel's group id is hotel_group_id
                return qs.filter(hotel_group_id=hotel_group_id)
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                hotel_id = user_metadata.hotel_id
                # filter hotel choices
                return qs.filter(hotel_id=hotel_id)
            return qs
        except UserMetadata.DoesNotExist:     
            return models.ServiceCategoryAdmin.objects.all() # Global admin might not have usermetadata
        return models.ServiceCategoryAdmin.objects.none()  


class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        # changing drop down filter to ajax
        current_user = self.request.user

        super(ServiceAdminForm, self).__init__(*args, **kwargs)              

        # get metadata for current user    
        # fitler the select lists based on user groups 
        try:
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel            
            # if adding a booking set hotel and room to null
            if not self.instance.id:            
                self.fields['hotel'].widget.choices = []
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists():                
                hotel_group_id = user_metadata.hotel_group_id

                # filter hotel group choices based on group   
                hotel_groups = models.HotelGroup.objects.filter(id=hotel_group_id)
                choices = list(((x.id, x.hotel_group_name) for x in hotel_groups))
                choices.insert(0, ('', '---------'),) # allow for null
                self.fields['hotel_group'].widget.choices = choices                
                
                # filter hotel choices based on group   
                hotels = models.Hotel.objects.filter(hotel_group_id=hotel_group_id)
                choices = list(((x.id, x.hotel_name) for x in hotels))
                choices.insert(0, ('', '---------'),) # allow for null
                self.fields['hotel'].widget.choices = choices

                #filter service categories based on hotel       
                service_categories = models.ServiceCategory.objects.filter(hotel_group_id=hotel_group_id)
                choices = list((x.id, x.category_name) for x in service_categories)
                choices.insert(0, ('', '---------'),) # allow for null
                self.fields['service_category'].widget.choices = choices                  
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                hotel_id = user_metadata.hotel_id

                # filter hotel choices based on hotel 
                hotels = models.Hotel.objects.filter(id=hotel_id)
                choices = list((x.id, x.hotel_name) for x in hotels)
                choices.insert(0, ('', '---------'),) # allow for null
                self.fields['hotel'].widget.choices = choices    

                #filter service categories based on hotel       
                service_categories = models.ServiceCategory.objects.filter(id=hotel_id)
                choices = list((x.id, x.category_name) for x in service_categories)
                choices.insert(0, ('', '---------'),) # allow for null
                self.fields['service_category'].widget.choices = choices    
            elif self.instance.id: # filter for global administrators if editing record
                hotel_group_id = self.instance.hotel_group_id

                # filter hotel choices based on group   
                hotels = models.Hotel.objects.filter(hotel_group_id=hotel_group_id)
                choices = list((x.id, x.hotel_name) for x in hotels)
                choices.insert(0, ('', '---------'),) # allow for null
                self.fields['hotel'].widget.choices = choices                
                hotel_id = self.instance.hotel_id             

        except UserMetadata.DoesNotExist:     
            None                   


class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm
    # add the request to the form
    def get_form(self, request, obj=None, **kwargs):
        form = super(ServiceAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form      
    list_display = [ 
        "id",
        "service_category",
        "service_type",
        "service_name",
        "hotel_group",
        "hotel",
        "meeting_room",
        "location",
        "rate",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]
    fields = [
        "icon",        
        "service_type",
        "service_category",
        "service_name",
        "hotel_group",
        "hotel",
        "meeting_room",
        "location",
        "rate",
        "created",
        "last_updated",
    ]
    search_fields = [
        "hotel_group__hotel_group_name",
        "hotel__hotel_name",
        "service_category__category_name",
        "service_name" 
    ] 
    list_filter = [
        'hotel_group',
        'hotel',
        'service_category'
    ]  

    def get_queryset(self, request):
        qs = super(ServiceAdmin, self).get_queryset(request)  
        # get current user
        current_user = request.user    
        # get metadata for current user
        # filter list based on user groups
        try:
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists():                
                hotel_group_id = user_metadata.hotel_group_id
                # filter hotel choices
                # need to filter where a hotel's group id is hotel_group_id
                return qs.filter(hotel_group_id=hotel_group_id)
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                hotel_id = user_metadata.hotel_id
                # filter hotel choices
                return qs.filter(hotel_id=hotel_id)
            return qs
        except UserMetadata.DoesNotExist:     
            return models.Service.objects.all() # Global admin might not have usermetadata
        return models.Service.objects.all()           


class HotelGroupAdminForm(forms.ModelForm):

    class Meta:
        model = models.HotelGroup
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(HotelGroupAdminForm, self).__init__(*args, **kwargs)
        self.fields['head_office_city'].widget.attrs.update({'readonly':''})
        self.fields['head_office_country'].widget.attrs.update({'readonly':''})
        self.fields['head_office_postal_code'].widget.attrs.update({'readonly':''})
        # self.fields['head_office_geolocation'].widget.attrs.update({'readonly':''})
        self.fields['head_office_latitude'].widget.attrs.update({'readonly':''})
        self.fields['head_office_longitude'].widget.attrs.update({'readonly':''})
        

class HotelGroupAdmin(admin.ModelAdmin):
    form = HotelGroupAdminForm
    list_display = [
        "hotel_group_name",
        "head_office_address",
        "head_office_postal_code",
        "head_office_city",
        "head_office_country",
        # "head_office_geolocation",        
        "created",
        "last_updated",
    ]
    readonly_fields = [    
        "created",
        "last_updated",
    ]
    fields = (
        "hotel_group_name",
        "head_office_address",
        "head_office_postal_code",
        "head_office_city",
        "head_office_country",
        # "head_office_geolocation"
        "head_office_latitude",
        "head_office_longitude",
    ) 
    search_fields = [
        'hotel_group_name',
        'head_office_city',
        'head_office_country',
    ]      
    def get_queryset(self, request):
        qs = super(HotelGroupAdmin, self).get_queryset(request)  
        # get current user
        current_user = request.user    
        # get metadata for current user
        try:
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists():
                hotel_group_id = user_metadata.hotel_group_id
                return qs.filter(id=hotel_group_id)
            return qs
        except UserMetadata.DoesNotExist:     
            return models.HotelGroup.objects.all() # Global admin might not have usermetadata
        return models.HotelGroup.objects.all()  


class HotelGalleryAdminForm(forms.ModelForm):

    class Meta:
        model = models.HotelGallery
        fields = "__all__"


class HotelGalleryAdmin(admin.ModelAdmin):
    form = HotelGalleryAdminForm
    list_display = [
        "created",
        "image",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class SubscriptionAdminForm(forms.ModelForm):

    class Meta:
        model = models.Subscription
        fields = "__all__"


class SubscriberInline(admin.TabularInline):
    model = models.Subscriber


class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionAdminForm
    list_display = [
        "subscription_unit",
        "subscription_rate",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]
    inlines = [SubscriberInline,]


admin.site.register(models.Hotel, HotelAdmin)
admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.Booking, BookingAdmin)
admin.site.register(models.Icon, IconAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.ServiceCategory, ServiceCategoryAdmin)
admin.site.register(models.HotelGroup, HotelGroupAdmin)
admin.site.register(models.HotelGallery, HotelGalleryAdmin)
admin.site.register(models.Subscription, SubscriptionAdmin)
