from django.views import generic
from . import models
from . import forms
from django.contrib.auth.views import PasswordResetView
from users.forms import CustomPasswordResetForm


class UserMetadataListView(generic.ListView):
    model = models.UserMetadata
    form_class = forms.UserMetadataForm


class UserMetadataCreateView(generic.CreateView):
    model = models.UserMetadata
    form_class = forms.UserMetadataForm


class UserMetadataDetailView(generic.DetailView):
    model = models.UserMetadata
    form_class = forms.UserMetadataForm


class UserMetadataUpdateView(generic.UpdateView):
    model = models.UserMetadata
    form_class = forms.UserMetadataForm
    pk_url_kwarg = "pk"
