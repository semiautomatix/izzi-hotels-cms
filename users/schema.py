from django.conf import settings
# cookbook/ingredients/schema.py
import graphene
# logging
import logging
# firebase
import firebase_admin

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token
from users.models import UserMetadata
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import login
from graphql import GraphQLError
from firebase_admin import auth
# email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

# Get an instance of a logger
logger = logging.getLogger('django')


# enums
class Genders(graphene.Enum):
    MALE = 'male'
    FEMALE = 'female'
    NON_BINARY = 'non_binary'

class AgeRanges(graphene.Enum):
    A_18 = '18'
    A_25 = '25'
    A_35 = '35'
    A_45 = '45'
    A_55 = '55'
    A_65 = '65'


class UserType(DjangoObjectType):
    class Meta:
        model = User

class UserMetadataType(DjangoObjectType):
    class Meta:
        model = UserMetadata          


class Query(object):
    user = graphene.Field(UserType,
                          id=graphene.Int())      
    current_user = graphene.Field(UserType)      
    all_users = graphene.List(UserType)
    all_usermetadatas = graphene.List(UserMetadataType)

    @login_required
    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    @login_required
    def resolve_all_usermetadatas(self, info, **kwargs):
        return UserMetadata.objects.all()

    @login_required
    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=id)

        return None      

    @login_required
    def resolve_current_user(self, info, **kwargs):
        user = info.context.user

        if id is not None:
            return User.objects.get(pk=user.id)

        return None   

# Create Input Object Types 
class ProfileInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    email_address = graphene.String()
    address = graphene.String()
    middle_name = graphene.String()
    gender = Genders()
    age_range = AgeRanges()
    nationality = graphene.String()
    position = graphene.String()
    uid = graphene.String()
    profile_picture = graphene.String()

                    
class Register(graphene.Mutation):
    class Arguments:
        email_address = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    user = graphene.Field(UserType)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, email_address, first_name, last_name):   
        one_time_password = User.objects.make_random_password()

        user = User.objects.create_user(email=email_address, username=email_address, password=one_time_password)  
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.full_clean()
        user.save()

        fbuser = auth.create_user(email=email_address, password=one_time_password)
        uid = fbuser.uid

        user_metadata = UserMetadata.objects.create(user_id=user.id, uid=uid)           
        user_metadata.save()  

        msg_plain = render_to_string('email/registration_confirmation.txt', { 'user': user, 'password': one_time_password, 'site_name': Site.objects.get_current().domain })
        msg_html = render_to_string('email/registration_confirmation.html', { 'user': user, 'password': one_time_password, 'site_name': Site.objects.get_current().domain })

        send_mail(
            'Registration confirmation',
            msg_plain,            
            settings.FROM_EMAIL_ADDRESS,
            recipient_list=[user.email],
            html_message=msg_html,
        )                   

        return Register(ok=True, user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        input = ProfileInput(required=True)

    user = graphene.Field(UserType)
    ok = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(self, info, input):      
        user = info.context.user
        ok = True          
        user_instance = User.objects.get(pk=user.id)        
        
        if input.first_name is not None:
            user_instance.first_name = input.first_name
        if input.last_name is not None:
            user_instance.last_name = input.last_name        
        if input.email_address is not None:
            user_instance.email = input.email_address  

        user_instance.save()
        
        try:
            user_metadata_instance = UserMetadata.objects.get(user_id=user.id) 
        except UserMetadata.DoesNotExist:
            user_metadata_instance = UserMetadata.objects.create(user_id=user.id)         
        
        if input.address is not None:
            user_metadata_instance.address = input.address
        if input.profile_picture is not None:
            user_metadata_instance.profile_picture = input.profile_picture
        if input.middle_name is not None:
            user_metadata_instance.middle_name = input.middle_name
        if input.gender is not None:
            user_metadata_instance.gender = input.gender
        if input.age_range is not None:
            user_metadata_instance.age_range = input.age_range
        if input.nationality is not None:
            user_metadata_instance.nationality = input.nationality
        if input.position is not None:
            user_metadata_instance.position = input.position
        if input.uid is not None:
            user_metadata_instance.uid = input.uid
        user_metadata_instance.save()

        return UpdateUser(ok=ok, user=user_instance) 

'''
class UpdateProfilePicture(graphene.Mutation):
    class Arguments:
        image = Upload()
    ok = graphene.Boolean()    

    @classmethod
    
    def mutate(self, info, image=None): 
        print('here')

        user = info.context.user
        user_metadata_instance = UserMetadata.objects.get(user_id=user.id)         
        
        user_metadata_instance.save()
        return UpdateUser(ok=ok, user=user_instance) 
'''

class ChangePassword(graphene.Mutation):
    class Arguments:
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)
        confirm_password = graphene.String(required=True)

    user = graphene.Field(UserType)
    ok = graphene.Boolean()   

    @staticmethod
    @login_required
    def mutate(self, info, old_password, new_password, confirm_password):  
        ok = False          
        if new_password == confirm_password:
            user = info.context.user            
            user_instance = User.objects.get(pk=user.id)
            if user.check_password(old_password):
                ok = True
                user.set_password(new_password)
                user.save()
                #user.email_user
            else: 
                raise GraphQLError('Old password is incorrect')
            return ChangePassword(ok=ok, user=user_instance)      
        else:
            raise GraphQLError('Passwords do not match')

class ForgotPassword(graphene.Mutation):
    class Arguments:
        email_address = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod    
    def mutate(self, info, email_address):      
        '''
        form = PasswordResetForm({'email': email_address})       
        assert form.is_valid()
        request = HttpRequest()
        request.META['SERVER_NAME'] = 'www.example.com'
        request.META['SERVER_PORT'] = 80
        form.save(
            request= request,
            use_https=True,
            site_name='iZZi Hotels',
            from_email="admin@mysite.com", 
            email_template_name='registration/password_reset_email.html'
        )         
        form.save()
        '''
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
                    recipient_list=[user.email],
                    html_message=msg_html,
                )

            except User.DoesNotExist: 
                ok = False

            ok = True
        except User.DoesNotExist: 
            ok = True # do not expose email addresses by indicating existence or not

        return ForgotPassword(ok)    

class FirebaseUID(graphene.Mutation):
    class Arguments:
        uid = graphene.String(required=True)

    ok = graphene.Boolean()
    token = graphene.String()

    @staticmethod    
    def mutate(self, info, uid):      
        ok = True
        token = None
        try:
            user_metadata = UserMetadata.objects.get(uid=uid)     
            user = User.objects.get(id=user_metadata.user_id)       
            login(info.context, user, backend='django.contrib.auth.backends.ModelBackend')
            token = get_token(user)
        except UserMetadata.DoesNotExist:   
            ok = False
            return
        except User.DoesNotExist:
            ok = False
            return

        return FirebaseUID(ok,token)  

class Mutation(graphene.ObjectType):
    register = Register.Field()
    change_password = ChangePassword.Field()
    forgot_password = ForgotPassword.Field()
    update_user = UpdateUser.Field()
    fb_uid = FirebaseUID.Field()
    # update_profile_picture = UpdateProfilePicture.Field()