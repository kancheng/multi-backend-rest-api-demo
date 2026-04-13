from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("quantity", models.FloatField()),
                ("unit", models.CharField(max_length=50)),
                ("expiry_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="UsageLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("used_quantity", models.FloatField()),
                ("date", models.DateField()),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="usage_logs",
                        to="config.ingredient",
                    ),
                ),
            ],
        ),
    ]
