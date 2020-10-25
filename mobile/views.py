from django.views import generic
from . import models
from . import forms


class RatingListView(generic.ListView):
    model = models.Rating
    form_class = forms.RatingForm


class RatingCreateView(generic.CreateView):
    model = models.Rating
    form_class = forms.RatingForm


class RatingDetailView(generic.DetailView):
    model = models.Rating
    form_class = forms.RatingForm


class RatingUpdateView(generic.UpdateView):
    model = models.Rating
    form_class = forms.RatingForm
    pk_url_kwarg = "pk"


class ServiceBookingListView(generic.ListView):
    model = models.ServiceBooking
    form_class = forms.ServiceBookingForm


class ServiceBookingCreateView(generic.CreateView):
    model = models.ServiceBooking
    form_class = forms.ServiceBookingForm


class ServiceBookingDetailView(generic.DetailView):
    model = models.ServiceBooking
    form_class = forms.ServiceBookingForm


class ServiceBookingUpdateView(generic.UpdateView):
    model = models.ServiceBooking
    form_class = forms.ServiceBookingForm
    pk_url_kwarg = "pk"


class EventListView(generic.ListView):
    model = models.Event
    form_class = forms.EventForm


class EventCreateView(generic.CreateView):
    model = models.Event
    form_class = forms.EventForm


class EventDetailView(generic.DetailView):
    model = models.Event
    form_class = forms.EventForm


class EventUpdateView(generic.UpdateView):
    model = models.Event
    form_class = forms.EventForm
    pk_url_kwarg = "pk"
