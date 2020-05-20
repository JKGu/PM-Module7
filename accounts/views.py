from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import Group


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passwordc']:
            try:
                user = User.objects.get(username=request.POST['username'])
                groups = request.POST.getlist('types')
                return render(request, 'accounts/signup.html',{'error':'Username already exists!','data':request.POST,'groups':groups})
            except User.DoesNotExist:
                groups = request.POST.getlist('types')
                if len(groups) == 0:
                    return render(request, 'accounts/signup.html',{'error':'You must select alteast one type.','data':request.POST,'groups':groups})
                user = User.objects.create_user(request.POST['username'], password = request.POST['password'])

                for x in groups:
                    group = Group.objects.get_or_create(name=x)[0]
                    group.user_set.add(user)
                auth.login(request, user)
                if has_group(user, 'quiz_admin'):
                    return redirect('quizzes:admin_index')
                if has_group(user, 'quiz_maker'):
                    return redirect('index')
                return redirect('quizzes:taker_index')
        else:
            groups = request.POST.getlist('types')
            return render(request, 'accounts/signup.html',{'error':'Password must match','data':request.POST,'groups':groups})

    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])

        try:
            user_ = User.objects.get(username=request.POST['username'])
            if not user_.is_active:
                return render(request, 'accounts/login.html',{'error':'Your account is suspended'})

        except User.DoesNotExist:
            pass
            
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

