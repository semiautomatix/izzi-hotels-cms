"""izzihotels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.forms import CustomPasswordResetForm

from cms.views import FileUploadView

# from rest_auth.views import PasswordResetConfirmView
from izzihotels.schema import schema

# Import dashboard module views
from izzidashboard import dashboard_modules_views

admin.site.site_header = 'iZZi Hotels Admin'
admin.site.site_title = 'iZZi Hotels'

urlpatterns = [
    #path('', include('auth0login.urls')),    
    path('', admin.site.urls),
    url(r'^imageupload', FileUploadView.as_view()),
    # GraphQL
    url(r'^graphql$', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),    
    url(r'^password-change/$', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('password_change_done')), name='password_change'),
    #url(r'password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    url(r'^password-change-done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),   
    url(r'^password_reset/', auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm), name='password_reset'),    
    url(r'^password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # exempt for mobile
    # RESTful used by backend pages
    path('', include(('cms.urls', 'cms'), namespace='cms')),
    path('', include(('mobile.urls', 'mobile'), namespace='mobile')),
    # jet
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    # path('jet_api/', include('jet_django.urls')),
    path('dashboard/', include('izzidashboard.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    # url('^django_plotly_dash/', include('django_plotly_dash.urls')),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(),
    #        name='password_reset_confirm'),
    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    # url('', include('social_django.urls', namespace='social')),
    # url(r'^accounts/', include('allauth.urls')),   
    # url(r'', include('user_sessions.urls', 'user_sessions')), # Django User Sessions
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
