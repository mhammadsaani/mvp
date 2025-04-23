from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def student_required(view_func):
    """
    Decorator for views that checks that the user is a student
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('accounts:login')
            
        if not request.user.is_student:
            messages.error(request, 'You must be a student to access this page.')
            return redirect('home')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def teacher_required(view_func):
    """
    Decorator for views that checks that the user is a teacher
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('accounts:login')
            
        if not request.user.is_teacher:
            messages.error(request, 'You must be a teacher to access this page.')
            return redirect('home')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    """
    Decorator for views that checks that the user is an admin
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('accounts:login')
            
        if not request.user.is_admin:
            messages.error(request, 'You must be an admin to access this page.')
            return redirect('home')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view