from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if 'authenticator' not in request.session:
        return render(request, 'registration/index.html')
    else:
        return redirect('/success')

def success(request):
    if 'authenticator' not in request.session:
        return render(request, 'registration/hacker.html')
    else:
        context = {
            'messages': Message.objects.all().order_by('-created_at'),
            'users': User.objects.get(email_hash=request.session['authenticator']),
            'comments': Comment.objects.all()
        }
        return render(request, 'registration/wall.html', context)

def hacker(request):
    return render(request, 'registration/hacker.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('/')
        else:
            create = User.objects.create_user(request.POST)
            messages.success(request, "User successfully created!")
            user = User.objects.last()
            request.session['authenticator'] = user.email_hash
            request.session['first_name'] = user.first_name
        return redirect('/success')    
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='login')
            return redirect('/')
        else:
            user = User.objects.get(email = request.POST['email'])
            request.session['authenticator'] = user.email_hash
            request.session['first_name'] = user.first_name
        return redirect('/success')    
    else:
        return redirect('/')

def logout(request):
    if request.method == 'POST':
        del request.session['first_name']
        del request.session['authenticator']
        return redirect('/')
    else:
        return redirect('/')

def message(request):
    if request.method == 'POST':
        Message.objects.create(message=request.POST['message'], user=User.objects.get(id=request.POST['user_id']))
        return redirect('/success')
    else:
        return redirect('/')

def comment(request):
    if request.method == 'POST':
        Comment.objects.create(comment=request.POST['comment'], user=User.objects.get(id=request.POST['user_id']), message=Message.objects.get(id=request.POST['message_id']))
        return redirect('/success')
    else:
        return redirect('/')

def delete(request):
    if request.method == 'POST':
        message = Message.objects.get(id=request.POST['message_id'])
        user = User.objects.get(id=request.POST['user_id'])
        if message.user_id == user.id:
            message.delete()
            return redirect('/success')
        else:
            return redirect('/success')
    else:
        return redirect('/')