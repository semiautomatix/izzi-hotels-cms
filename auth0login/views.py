# auth0login/views.py

from django.shortcuts import render, redirect

def index(request):
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    else:
        return redirect('/login/auth0')