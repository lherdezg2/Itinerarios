from django.db import models


class ItineraryRecord(models.Model):
    itinerary_id = models.CharField(max_length=64, primary_key=True)
    origin_airport_id = models.CharField(max_length=8)
    destination_airport_id = models.CharField(max_length=8)
    travel_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=32, default="Pendiente")

    class Meta:
        db_table = "itinerary_itineraryrecord"
