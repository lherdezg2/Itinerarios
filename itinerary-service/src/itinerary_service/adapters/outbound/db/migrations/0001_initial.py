from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ItineraryRecord",
            fields=[
                ("itinerary_id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("origin_airport_id", models.CharField(max_length=8)),
                ("destination_airport_id", models.CharField(max_length=8)),
                ("travel_date", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
            ],
            options={
                "db_table": "itinerary_itineraryrecord",
            },
        ),
    ]
