from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, LoginForm
from .models import CustomUser


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(request, 'members/login.html', {'form': form})

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            form.add_error('password', "Wrong username or password!")
            return render(request, 'members/login.html', {'form': form})
        
        login(request, user)
        return redirect('profile')
    else:
        form = LoginForm()
        return render(request, 'members/login.html', {'form': form})
    
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if not form.is_valid():
            return render(request, 'members/signup.html', {'form': form})

        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        if password != confirm_password:
            form.add_error('confirm_password', "Passwords do not match!")
            return render(request, 'members/signup.html', {'form': form})

        if CustomUser.objects.filter(username=username).exists():
            form.add_error('username', "User with this username already exists.")
            return render(request, 'members/signup.html', {'form': form})

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)
        return redirect('profile')
    else:
        form = SignupForm()
        return render(request, 'members/signup.html', {'form': form})
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

