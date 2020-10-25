# import the logging library
import logging

from users.models import UserMetadata
from django.shortcuts import redirect
from django.urls import reverse

# Get an instance of a logger
logger = logging.getLogger('django')

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        current_user = request.user
        # ignore for users not logged in or trying to logout
        if current_user.is_authenticated and not request.path == '/logout/' and not request.path == '/graphql':
          try:
            # get metadata for current user    
            user_metadata = UserMetadata.objects.get(user_id=current_user.id)

            if user_metadata.change_password: 
              # redirect to change password
              if not request.path == reverse('password_change'):
                return redirect(reverse('password_change'))
                
          except UserMetadata.DoesNotExist:     
            None 

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response