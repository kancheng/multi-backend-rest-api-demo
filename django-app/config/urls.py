from django.contrib import admin
from django.urls import path

from .views import (
    expiring_ingredients,
    hello,
    ingredient_detail,
    ingredient_usage,
    ingredients_collection,
    low_stock_ingredients,
    use_ingredient,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", hello),
    path("api/ingredients", ingredients_collection),
    path("api/ingredients/<int:ingredient_id>", ingredient_detail),
    path("api/ingredients/<int:ingredient_id>/use", use_ingredient),
    path("api/ingredients/<int:ingredient_id>/usage", ingredient_usage),
    path("api/ingredients/expiring", expiring_ingredients),
    path("api/ingredients/low-stock", low_stock_ingredients),
]
