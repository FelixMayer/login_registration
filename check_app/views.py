from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email_address = request.POST['email_address'],
            password = hashed_pw
        )
        request.session['user_id'] = user.id
        return redirect('/dashboard')

def login(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_list = User.objects.filter(email_address = request.POST['login_email'])
        if len(user_list) == 0:
            messages.error(request, 'A user with this email does not exists.')
            return redirect('/')
        else:
            user = user_list[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/dashboard')
            else:
                messages.error(request, 'Incorrect password or email.')
                return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'user': user
    }

    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')
