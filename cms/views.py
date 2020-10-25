from django.views import generic
from . import models
from . import forms
from . import serializers
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# files
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions


class HotelListView(generic.ListView):
    model = models.Hotel
    form_class = forms.HotelForm
    

class HotelCreateView(generic.CreateView):
    model = models.Hotel
    form_class = forms.HotelForm


class HotelDetailView(generic.DetailView):
    model = models.Hotel
    form_class = forms.HotelForm


class HotelUpdateView(generic.UpdateView):
    model = models.Hotel
    form_class = forms.HotelForm
    pk_url_kwarg = "pk"


class RoomListView(generic.ListView):
    model = models.Room
    form_class = forms.RoomForm


class RoomCreateView(generic.CreateView):
    model = models.Room
    form_class = forms.RoomForm


class RoomDetailView(generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm


class RoomUpdateView(generic.UpdateView):
    model = models.Room
    form_class = forms.RoomForm
    pk_url_kwarg = "pk"


class BookingListView(generic.ListView):
    model = models.Booking
    form_class = forms.BookingForm


class BookingCreateView(generic.CreateView):
    model = models.Booking
    form_class = forms.BookingForm


class BookingDetailView(generic.DetailView):
    model = models.Booking
    form_class = forms.BookingForm


class BookingUpdateView(generic.UpdateView):
    model = models.Booking
    form_class = forms.BookingForm
    pk_url_kwarg = "pk"


class IconListView(generic.ListView):
    model = models.Icon
    form_class = forms.IconForm


class IconCreateView(generic.CreateView):
    model = models.Icon
    form_class = forms.IconForm


class IconDetailView(generic.DetailView):
    model = models.Icon
    form_class = forms.IconForm


class IconUpdateView(generic.UpdateView):
    model = models.Icon
    form_class = forms.IconForm
    pk_url_kwarg = "pk"


class ServiceListView(generic.ListView):
    model = models.Service
    form_class = forms.ServiceForm


class ServiceCreateView(generic.CreateView):
    model = models.Service
    form_class = forms.ServiceForm


class ServiceDetailView(generic.DetailView):
    model = models.Service
    form_class = forms.ServiceForm


class ServiceUpdateView(generic.UpdateView):
    model = models.Service
    form_class = forms.ServiceForm
    pk_url_kwarg = "pk"


class HotelGroupListView(generic.ListView):
    model = models.HotelGroup
    form_class = forms.HotelGroupForm


class HotelGroupCreateView(generic.CreateView):
    model = models.HotelGroup
    form_class = forms.HotelGroupForm


class HotelGroupDetailView(generic.DetailView):
    model = models.HotelGroup
    form_class = forms.HotelGroupForm


class HotelGroupUpdateView(generic.UpdateView):
    model = models.HotelGroup
    form_class = forms.HotelGroupForm
    pk_url_kwarg = "pk"

class HotelGalleryListView(generic.ListView):
    model = models.HotelGallery
    form_class = forms.HotelGalleryForm


class HotelGalleryCreateView(generic.CreateView):
    model = models.HotelGallery
    form_class = forms.HotelGalleryForm


class HotelGalleryDetailView(generic.DetailView):
    model = models.HotelGallery
    form_class = forms.HotelGalleryForm


class HotelGalleryUpdateView(generic.UpdateView):
    model = models.HotelGallery
    form_class = forms.HotelGalleryForm
    pk_url_kwarg = "pk"


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

      file_serializer = serializers.FileSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = [permissions.AllowAny] # should be authenticated
