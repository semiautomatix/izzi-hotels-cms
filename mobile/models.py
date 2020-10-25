from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

class Rating(models.Model):

    #  Relationships
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    hotel = models.ForeignKey("cms.Hotel", on_delete=models.CASCADE)
    hotel_gallery = models.ForeignKey("cms.HotelGallery", null=True, on_delete=models.SET_NULL)

    #  Fields 
    rating = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(max_length=4000)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("mobile_Rating_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("mobile_Rating_update", args=(self.pk,))


# bookings for meeting and co-share services
class ServiceBooking(models.Model):

    #  Relationships
    # hotel = models.ForeignKey("cms.Hotel", on_delete=models.CASCADE) 
    service = models.ForeignKey("cms.Service", on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    #  Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    check_out_date_time = models.DateTimeField(null=True) # time of checking in, meetings only
    end_date_time = models.DateTimeField() # time service ends
    check_in_date_time = models.DateTimeField(null=True) #  time of checking out, meetings only
    start_date_time = models.DateTimeField() # time service starts

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("mobile_ServiceBooking_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("mobile_ServiceBooking_update", args=(self.pk,))


class Event(models.Model):

    #  Relationships
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    
    #  Fields
    event_name = models.CharField(max_length=100)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    event_metadata = models.TextField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("mobile_Event_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("mobile_Event_update", args=(self.pk,))
