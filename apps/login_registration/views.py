# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import users
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'login_registration/index.html')

def success(request):
    data = users.objects.get(id=request.session['id'])

    context = {
        'user_data': data
    }

    return render(request, 'login_registration/success.html', context)

def create(request):

    errors = users.objects.basic_validator(request.POST)
    
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    else:
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = users.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=password)
        user.save()
        request.session['id'] = user.id

    return redirect('/success')

def login(request):
    
    errors = users.objects.login(request.POST)
    print errors
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    user = users.objects.filter(email=request.POST['email'])
    request.session['id'] = user[0].id

    return redirect('/success')

def logoff(request):
    request.session.clear()
    return redirect('/')