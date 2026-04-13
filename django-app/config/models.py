from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=120)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    expiry_date = models.DateField()


class UsageLog(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="usage_logs",
    )
    used_quantity = models.FloatField()
    date = models.DateField()
