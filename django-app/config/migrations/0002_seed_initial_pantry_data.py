from datetime import date

from django.db import migrations


def seed_data(apps, schema_editor):
    Ingredient = apps.get_model("config", "Ingredient")
    UsageLog = apps.get_model("config", "UsageLog")

    if Ingredient.objects.exists():
        return

    milk = Ingredient.objects.create(
        name="Milk",
        quantity=2,
        unit="bottle",
        expiry_date=date(2026, 4, 20),
    )
    eggs = Ingredient.objects.create(
        name="Eggs",
        quantity=12,
        unit="piece",
        expiry_date=date(2026, 4, 18),
    )
    Ingredient.objects.create(
        name="Rice",
        quantity=1.5,
        unit="kg",
        expiry_date=date(2026, 12, 31),
    )

    UsageLog.objects.create(
        ingredient=milk,
        used_quantity=1,
        date=date(2026, 4, 13),
    )
    UsageLog.objects.create(
        ingredient=eggs,
        used_quantity=2,
        date=date(2026, 4, 13),
    )


def unseed_data(apps, schema_editor):
    Ingredient = apps.get_model("config", "Ingredient")
    UsageLog = apps.get_model("config", "UsageLog")

    UsageLog.objects.all().delete()
    Ingredient.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("config", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
