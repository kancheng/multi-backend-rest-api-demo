<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Ingredient extends Model
{
    protected $fillable = ['name', 'quantity', 'unit', 'expiry_date'];

    public function usageLogs(): HasMany
    {
        return $this->hasMany(UsageLog::class);
    }
}
