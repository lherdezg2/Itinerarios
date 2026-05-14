from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("itinerary_db", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="itineraryrecord",
            name="status",
            field=models.CharField(default="Pendiente", max_length=32),
        ),
    ]
