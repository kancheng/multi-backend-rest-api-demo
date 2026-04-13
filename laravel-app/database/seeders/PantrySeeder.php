<?php

namespace Database\Seeders;

use App\Models\Ingredient;
use App\Models\UsageLog;
use Illuminate\Database\Seeder;

class PantrySeeder extends Seeder
{
    /**
     * Seed the application's pantry data.
     */
    public function run(): void
    {
        if (Ingredient::count() > 0) {
            return;
        }

        $milk = Ingredient::create([
            'name' => 'Milk',
            'quantity' => 2,
            'unit' => 'bottle',
            'expiry_date' => '2026-04-20',
        ]);

        $eggs = Ingredient::create([
            'name' => 'Eggs',
            'quantity' => 12,
            'unit' => 'piece',
            'expiry_date' => '2026-04-18',
        ]);

        Ingredient::create([
            'name' => 'Rice',
            'quantity' => 1.5,
            'unit' => 'kg',
            'expiry_date' => '2026-12-31',
        ]);

        UsageLog::create([
            'ingredient_id' => $milk->id,
            'used_quantity' => 1,
            'date' => '2026-04-13',
        ]);

        UsageLog::create([
            'ingredient_id' => $eggs->id,
            'used_quantity' => 2,
            'date' => '2026-04-13',
        ]);
    }
}
