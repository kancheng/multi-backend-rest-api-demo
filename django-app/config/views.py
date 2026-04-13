import json
from datetime import date, timedelta

from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Ingredient, UsageLog


def ingredient_to_dict(ingredient):
    return {
        "id": ingredient.id,
        "name": ingredient.name,
        "quantity": ingredient.quantity,
        "unit": ingredient.unit,
        "expiry_date": ingredient.expiry_date.isoformat(),
    }


def usage_to_dict(usage):
    return {
        "id": usage.id,
        "ingredient_id": usage.ingredient_id,
        "used_quantity": usage.used_quantity,
        "date": usage.date.isoformat(),
    }


def parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return None


def hello(request):
    return render(request, "index.html")


@csrf_exempt
def ingredients_collection(request):
    if request.method == "GET":
        ingredients = Ingredient.objects.order_by("id")
        return JsonResponse([ingredient_to_dict(item) for item in ingredients], safe=False)

    if request.method == "POST":
        payload = parse_json_body(request)
        if payload is None:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        required_fields = ["name", "quantity", "unit", "expiry_date"]
        if any(payload.get(field) in [None, ""] for field in required_fields):
            return JsonResponse(
                {"error": "name, quantity, unit, expiry_date are required"},
                status=422,
            )
        try:
            ingredient = Ingredient.objects.create(
                name=payload["name"],
                quantity=float(payload["quantity"]),
                unit=payload["unit"],
                expiry_date=payload["expiry_date"],
            )
        except (TypeError, ValueError):
            return JsonResponse({"error": "quantity must be a number"}, status=422)
        except Exception:
            return JsonResponse({"error": "Invalid payload"}, status=422)

        return JsonResponse(ingredient_to_dict(ingredient), status=201)

    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def ingredient_detail(request, ingredient_id):
    try:
        ingredient = Ingredient.objects.get(pk=ingredient_id)
    except Ingredient.DoesNotExist:
        return JsonResponse({"error": "Ingredient not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(ingredient_to_dict(ingredient))

    if request.method == "PUT":
        payload = parse_json_body(request)
        if payload is None:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        ingredient.name = payload.get("name", ingredient.name)
        ingredient.unit = payload.get("unit", ingredient.unit)
        ingredient.expiry_date = payload.get("expiry_date", ingredient.expiry_date)
        try:
            ingredient.quantity = float(payload.get("quantity", ingredient.quantity))
        except (TypeError, ValueError):
            return JsonResponse({"error": "quantity must be a number"}, status=422)
        try:
            ingredient.save()
        except Exception:
            return JsonResponse({"error": "Invalid payload"}, status=422)
        return JsonResponse(ingredient_to_dict(ingredient))

    if request.method == "DELETE":
        ingredient.delete()
        return JsonResponse({}, status=204)

    return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])


@csrf_exempt
def use_ingredient(request, ingredient_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        ingredient = Ingredient.objects.get(pk=ingredient_id)
    except Ingredient.DoesNotExist:
        return JsonResponse({"error": "Ingredient not found"}, status=404)

    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    used_quantity = payload.get("used_quantity")
    usage_date = payload.get("date", date.today().isoformat())
    try:
        used_quantity = float(used_quantity)
    except (TypeError, ValueError):
        return JsonResponse({"error": "used_quantity must be a positive number"}, status=422)
    if used_quantity <= 0:
        return JsonResponse({"error": "used_quantity must be a positive number"}, status=422)

    remaining = ingredient.quantity - used_quantity
    if remaining < 0:
        return JsonResponse({"error": "Insufficient stock"}, status=422)

    ingredient.quantity = remaining
    try:
        ingredient.save()
        usage = UsageLog.objects.create(
            ingredient=ingredient,
            used_quantity=used_quantity,
            date=usage_date,
        )
    except Exception:
        return JsonResponse({"error": "Invalid payload"}, status=422)

    return JsonResponse(
        {
            "ingredient": ingredient_to_dict(ingredient),
            "usage": usage_to_dict(usage),
        },
        status=201,
    )


def ingredient_usage(request, ingredient_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    try:
        ingredient = Ingredient.objects.get(pk=ingredient_id)
    except Ingredient.DoesNotExist:
        return JsonResponse({"error": "Ingredient not found"}, status=404)

    logs = ingredient.usage_logs.order_by("-date", "-id")
    return JsonResponse([usage_to_dict(item) for item in logs], safe=False)


def expiring_ingredients(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    raw_days = request.GET.get("days", "3")
    try:
        days = max(int(raw_days), 0)
    except ValueError:
        return JsonResponse({"error": "days must be an integer"}, status=422)

    boundary = date.today() + timedelta(days=days)
    ingredients = Ingredient.objects.filter(expiry_date__lte=boundary).order_by("expiry_date", "id")
    return JsonResponse([ingredient_to_dict(item) for item in ingredients], safe=False)


def low_stock_ingredients(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    raw_threshold = request.GET.get("threshold", "1")
    try:
        threshold = float(raw_threshold)
    except ValueError:
        return JsonResponse({"error": "threshold must be a number"}, status=422)

    ingredients = Ingredient.objects.filter(quantity__lte=threshold).order_by("quantity", "id")
    return JsonResponse([ingredient_to_dict(item) for item in ingredients], safe=False)
