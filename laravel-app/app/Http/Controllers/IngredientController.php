<?php

namespace App\Http\Controllers;

use App\Models\Ingredient;
use App\Models\UsageLog;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class IngredientController extends Controller
{
    public function index(): JsonResponse
    {
        return response()->json(Ingredient::orderBy('id')->get());
    }

    public function show(int $id): JsonResponse
    {
        $ingredient = Ingredient::find($id);
        if (!$ingredient) {
            return response()->json(['error' => 'Ingredient not found'], 404);
        }

        return response()->json($ingredient);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:120'],
            'quantity' => ['required', 'numeric'],
            'unit' => ['required', 'string', 'max:50'],
            'expiry_date' => ['required', 'date_format:Y-m-d'],
        ]);

        $ingredient = Ingredient::create($validated);
        return response()->json($ingredient, 201);
    }

    public function update(Request $request, int $id): JsonResponse
    {
        $ingredient = Ingredient::find($id);
        if (!$ingredient) {
            return response()->json(['error' => 'Ingredient not found'], 404);
        }

        $validated = $request->validate([
            'name' => ['sometimes', 'required', 'string', 'max:120'],
            'quantity' => ['sometimes', 'required', 'numeric'],
            'unit' => ['sometimes', 'required', 'string', 'max:50'],
            'expiry_date' => ['sometimes', 'required', 'date_format:Y-m-d'],
        ]);

        $ingredient->update($validated);
        return response()->json($ingredient->fresh());
    }

    public function destroy(int $id): JsonResponse
    {
        $ingredient = Ingredient::find($id);
        if (!$ingredient) {
            return response()->json(['error' => 'Ingredient not found'], 404);
        }
        $ingredient->delete();

        return response()->json([], 204);
    }

    public function useIngredient(Request $request, int $id): JsonResponse
    {
        $ingredient = Ingredient::find($id);
        if (!$ingredient) {
            return response()->json(['error' => 'Ingredient not found'], 404);
        }

        $validated = $request->validate([
            'used_quantity' => ['required', 'numeric', 'gt:0'],
            'date' => ['nullable', 'date_format:Y-m-d'],
        ]);

        $usedQuantity = (float) $validated['used_quantity'];
        $remaining = (float) $ingredient->quantity - $usedQuantity;
        if ($remaining < 0) {
            return response()->json(['error' => 'Insufficient stock'], 422);
        }

        $ingredient->update(['quantity' => $remaining]);
        $usage = UsageLog::create([
            'ingredient_id' => $ingredient->id,
            'used_quantity' => $usedQuantity,
            'date' => $validated['date'] ?? now()->toDateString(),
        ]);

        return response()->json([
            'ingredient' => $ingredient->fresh(),
            'usage' => $usage,
        ], 201);
    }

    public function usage(int $id): JsonResponse
    {
        $ingredient = Ingredient::find($id);
        if (!$ingredient) {
            return response()->json(['error' => 'Ingredient not found'], 404);
        }

        return response()->json(
            UsageLog::where('ingredient_id', $id)
                ->orderByDesc('date')
                ->orderByDesc('id')
                ->get()
        );
    }

    public function expiring(Request $request): JsonResponse
    {
        $days = max((int) $request->query('days', 3), 0);
        $limitDate = now()->addDays($days)->toDateString();
        $ingredients = Ingredient::whereDate('expiry_date', '<=', $limitDate)
            ->orderBy('expiry_date')
            ->orderBy('id')
            ->get();

        return response()->json($ingredients);
    }

    public function lowStock(Request $request): JsonResponse
    {
        $threshold = (float) $request->query('threshold', 1);
        $ingredients = Ingredient::where('quantity', '<=', $threshold)
            ->orderBy('quantity')
            ->orderBy('id')
            ->get();

        return response()->json($ingredients);
    }
}
