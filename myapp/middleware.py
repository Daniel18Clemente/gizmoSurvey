from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from .models import UserProfile


class ActiveUserMiddleware:
    """
    Middleware to check if authenticated users have active profiles
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip check for certain URLs to avoid infinite redirects
        skip_urls = [
            '/login/',
            '/logout/',
            '/register/',
            '/admin/',
        ]
        
        if (request.user.is_authenticated and 
            not any(request.path.startswith(url) for url in skip_urls)):
            
            try:
                profile = UserProfile.objects.get(user=request.user)
                if not profile.is_active:
                    logout(request)
                    messages.error(request, 'Your account has been deactivated. Please contact your teacher.')
                    return redirect('home')
            except UserProfile.DoesNotExist:
                logout(request)
                messages.error(request, 'User profile not found. Please contact your teacher.')
                return redirect('home')
        
        response = self.get_response(request)
        return response
