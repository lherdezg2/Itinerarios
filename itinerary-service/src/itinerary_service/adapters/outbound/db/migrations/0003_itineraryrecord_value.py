from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("itinerary_db", "0002_itineraryrecord_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="itineraryrecord",
            name="value",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
