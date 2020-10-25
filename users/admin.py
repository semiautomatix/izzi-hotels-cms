# firebase
import firebase_admin

from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, AdminPasswordChangeForm as BaseAdminPasswordChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from django.contrib.auth.models import Group, User
from django.forms.models import BaseInlineFormSet
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
# convert the errors to text
from django.utils.encoding import force_text
from firebase_admin import auth
from cms.models import Hotel, HotelGroup, Subscriber
from users.models import UserMetadata
from . import models
# email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('django')
logger.info("logger initalized " + __name__ + " admin.py")


# function to allow for the addition of attributes to the options elements of a select
# custom changes required  by jquery-chained https://github.com/tuupola/jquery_chained
class DataGroupSelect(forms.widgets.Select):
    
    def __init__(self, attrs=None, choices=(), data={}):
        super(DataGroupSelect, self).__init__(attrs, choices)
        self.data = data
 
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None): # noqa
        option = super(DataGroupSelect, self).create_option(name, value, label, selected, index, subindex=None, attrs=None) # noqa
        # adds the data-attributes to the attrs context var
        for data_attr, values in self.data.items():
            option['attrs'][data_attr] = values[option['value']]
 
        return option


# user metadata form
class UserMetadataAdminForm(forms.ModelForm): 
    hotel = None
    class Meta:
        model = models.UserMetadata     
        fields = [
            "hotel_group",
            "hotel",
            "age_range",
            "profile_picture",
            "middle_name",
            "nationality",
            "position",
            "gender",
            "user",
        ]  
    # filter the hotel fields based on group
    # custom changes required  by jquery-chained https://github.com/tuupola/jquery_chained
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = {'data-chained': dict(Hotel.objects.values_list('id', 'hotel_group_id'))}
        data['data-chained'][''] = ''  # empty option
     

class UserMetadataAdmin(admin.ModelAdmin):
    form = UserMetadataAdminForm
    list_display = [
        "hotel_group",
        "hotel",
        "age_range",
        "middle_name",
        "nationality",
        "position",
        "gender",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]    


admin.site.register(models.UserMetadata, UserMetadataAdmin)        

# inline user metadata form appearing on user form
class UserMetadataInlineFormSet(BaseInlineFormSet):    
    def _construct_form(self, i, **kwargs):
        form = super(UserMetadataInlineFormSet, self)._construct_form(i, **kwargs)
        form.request = self.request
        return form

    # filter the hotel fields based on group
    # custom changes required  by jquery-chained https://github.com/tuupola/jquery_chained
    def __init__(self, *args, **kwargs):
        # changing drop down filter to ajax
        current_user = self.request.user
        super(UserMetadataInlineFormSet, self).__init__(*args, **kwargs)        
        # get metadata for current user    
        # fitler the select lists based on user groups         

        #user_metadata = models.UserMetadata.objects.get(user_id=current_user.id)
        
        data = {'data-chained': dict(Hotel.objects.values_list('id', 'hotel_group_id'))}
        data['data-chained'][''] = ''  # empty option
        
        self.forms[0].fields['hotel_group'].widget = RelatedFieldWidgetWrapper(
            forms.widgets.Select(
                #attrs = hotel_group_attrs, 
                choices = self.forms[0].fields['hotel_group'].choices
            ),
            self.forms[0].fields['hotel_group'].widget.rel,
            self.forms[0].fields['hotel_group'].widget.admin_site,
            self.forms[0].fields['hotel_group'].widget.can_add_related,
            self.forms[0].fields['hotel_group'].widget.can_change_related,
            self.forms[0].fields['hotel_group'].widget.can_delete_related,
        )
        self.forms[0].fields['hotel'].widget = RelatedFieldWidgetWrapper(
            DataGroupSelect(
                choices = self.forms[0].fields['hotel'].choices,
                data = data,
                #attrs = hotel_attrs
            ),
            self.forms[0].fields['hotel'].widget.rel,
            self.forms[0].fields['hotel'].widget.admin_site,
            self.forms[0].fields['hotel'].widget.can_add_related,
            self.forms[0].fields['hotel'].widget.can_change_related,
            self.forms[0].fields['hotel'].widget.can_delete_related,
        ) 

        try:
            user_metadata = models.UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists():                
                hotel_group_id = user_metadata.hotel_group_id
                # filter hotel group choices based on group   
                hotel_groups = HotelGroup.objects.filter(id=hotel_group_id)
                choices = ((x.id, x.hotel_group_name) for x in hotel_groups)
                self.forms[0].fields['hotel_group'].widget.choices = choices
                # filter hotel choices based on group   
                hotels = Hotel.objects.filter(hotel_group_id=hotel_group_id)
                choices = ((x.id, x.hotel_name) for x in hotels)
                self.forms[0].fields['hotel'].widget.choices = choices
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                hotel_id = user_metadata.hotel_id
                # filter hotel choices
                hotels = Hotel.objects.filter(id=hotel_id)
                choices = ((x.id, x.hotel_name) for x in hotels)
                self.forms[0].fields['hotel'].widget.choices = choices 
        except models.UserMetadata.DoesNotExist:     
            None 
        
            
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# rename to "Additiona Info"
# only display certain fields
class UserMetadataInline(admin.StackedInline):             
    model = models.UserMetadata
    can_delete = False
    verbose_name = "Additional Info"
    verbose_name_plural = "Additional Info"    
    view_on_site = False
    formset = UserMetadataInlineFormSet    

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(UserMetadataInline, self).get_formset(request, obj, **kwargs)
        formset.request = request
        return formset  

    
    def get_fieldsets(self, request, obj=None):
        return [(None, {'fields': (
            'middle_name',
            'hotel_group', 
            'hotel',
            'age_range',
            'profile_picture',
            'nationality',
            'position',
            'gender',
        )})]     
    

class SubscriberInline(admin.StackedInline):
    model = Subscriber


# include first name and last name, username is now an email address 
class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    username = forms.EmailField(label='Email', max_length=255)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def save(self, commit=True):
        one_time_password = User.objects.make_random_password()

        user = super(UserCreationForm, self).save(commit=False)
        user.email = user.username  
        user.password1 = user.set_password(one_time_password)
        user.password2 = user.set_password(one_time_password)
        user.save()
        
        fbuser = auth.create_user(email=user.username, password=one_time_password)
        uid = fbuser.uid

        user_metadata = UserMetadata.objects.create(user_id=user.id, uid=uid)           
        user_metadata.save()     
        
        msg_plain = render_to_string('email/new_user.txt', { 'user': user, 'password': one_time_password, 'site_name': Site.objects.get_current().domain })
        msg_html = render_to_string('email/new_user.html', { 'user': user, 'password': one_time_password, 'site_name': Site.objects.get_current().domain })

        send_mail(
            'New user',
            msg_plain,
            user.email,
            ['some@receiver.com'],
            html_message=msg_html,
        )     

        return user 

    def is_valid(self):
        logger.info(force_text(self.errors))
        return super(UserCreationForm, self).is_valid()        

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    # form = UserChangeForm
    add_fieldsets = (
        (None, { 
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username')}),)    
    # filter the choices of user groups based on existing user group
    # group administrators can only assign hotel administrators and group administrators
    # hotel administrators can only assign hotel administrators
    def get_form(self, request, obj=None, **kwargs):
        # Get form from original UserAdmin.
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        current_user = request.user
        if 'groups' in form.base_fields:
            if current_user.groups.filter(name='Hotel Group Administrators').exists():
                groups = form.base_fields['groups']
                groups.queryset = groups.queryset.filter(name__in=['Hotel Group Administrators', 'Hotel Administrators'])
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                groups = form.base_fields['groups']
                groups.queryset = groups.queryset.filter(name='Hotel Administrators')
        return form  
    # limit fields sets, i.e. remove permissions  
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ('is_active', 'is_staff', 'groups')

        return [(_('Personal info'), {'fields': ('first_name', 'last_name', 'username', 'password')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})]             
    # user addtional information fields on change 
    inlines = [UserMetadataInline, SubscriberInline,]
    # def change_view(self, request, object_id):
    #   self.inlines=[UserMetadataInline,]
    #   return super(UserAdmin, self).change_view(request, object_id)    
    # define query set to filter for hotel and group administrators
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)  
        # get current user
        current_user = request.user    
        try:
            # get user metadata
            user_metadata = models.UserMetadata.objects.get(user_id=current_user.id)
            # check if user is global, group or hotel
            if current_user.groups.filter(name='Hotel Group Administrators').exists():
                hotel_group_id = user_metadata.hotel_group_id
                return qs.filter(usermetadata__hotel_group_id=hotel_group_id)
            elif current_user.groups.filter(name='Hotel Administrators').exists():
                hotel_id = user_metadata.hotel_id
                return qs.filter(usermetadata__hotel_group_id=hotel_id)
            return qs
        except models.UserMetadata.DoesNotExist:     
            return User.objects.all()
        return User.objects.all()             


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
