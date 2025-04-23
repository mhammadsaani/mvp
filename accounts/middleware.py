from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class UserTypeMiddleware:
    """
    Middleware to restrict access to certain views based on user type
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip middleware for authentication views
        if request.path.startswith('/admin/') or request.path.startswith('/accounts/'):
            return None
            
        # Check if user is authenticated
        if not request.user.is_authenticated:
            if not request.path == reverse('home'):
                messages.warning(request, 'Please log in to access this page.')
                return redirect('accounts:login')
            return None
            
        # Check if user is blocked
        if request.user.is_blocked:
            messages.error(request, 'Your account has been blocked. Please contact the administrator.')
            return redirect('home')
            
        # Check user type for specific app paths
        if request.path.startswith('/student/') and not request.user.is_student:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
            
        if request.path.startswith('/teacher/') and not request.user.is_teacher:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
            
        if request.path.startswith('/admin-panel/') and not request.user.is_admin:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
            
        return None