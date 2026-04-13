<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return response()
        ->view('pantry')
        ->header('Content-Type', 'text/html; charset=UTF-8');
});

Route::get('/welcome', function () {
    return view('welcome');
});