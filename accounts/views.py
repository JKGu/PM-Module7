from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import Group


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passwordc']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html',{'error':'Username already exists!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password']) 
                groups = request.POST.getlist('types')
                for x in groups:
                    group = Group.objects.get(name=x) 
                    group.user_set.add(user)
                auth.login(request, user)
                return redirect('index')
        else:
            return render(request, 'accounts/signup.html',{'error':'Password must match'})

    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            if has_group(user, 'quiz_admin'):
                return redirect('quizzes:admin_index')
            if has_group(user, 'quiz_maker'):
                return redirect('index')
            return redirect('quizzes:taker_index')
        else:
            return render(request, 'accounts/login.html',{'error':'Username and password did not match'})
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def has_group(user, group_name):
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False