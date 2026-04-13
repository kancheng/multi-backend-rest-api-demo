<?php

use App\Http\Controllers\IngredientController;
use Illuminate\Support\Facades\Route;

Route::get('/ingredients', [IngredientController::class, 'index']);
Route::get('/ingredients/expiring', [IngredientController::class, 'expiring']);
Route::get('/ingredients/low-stock', [IngredientController::class, 'lowStock']);
Route::get('/ingredients/{id}', [IngredientController::class, 'show']);
Route::post('/ingredients', [IngredientController::class, 'store']);
Route::put('/ingredients/{id}', [IngredientController::class, 'update']);
Route::delete('/ingredients/{id}', [IngredientController::class, 'destroy']);
Route::post('/ingredients/{id}/use', [IngredientController::class, 'useIngredient']);
Route::get('/ingredients/{id}/usage', [IngredientController::class, 'usage']);
