from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm

def register(request):
    """
    Register a new student user
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'student'  # Only students can register directly
            user.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    """
    Log in a user
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_blocked:
                    messages.error(request, 'Your account has been blocked. Please contact the administrator.')
                    return redirect('accounts:login')
                    
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect based on user type
                if user.is_student:
                    return redirect('student:dashboard')
                elif user.is_teacher:
                    return redirect('teacher:dashboard')
                elif user.is_admin:
                    return redirect('admin_panel:dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    """
    Log out a user
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    """
    Display user profile
    """
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    """
    Edit user profile
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})
