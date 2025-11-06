from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserBackend(ModelBackend):
    """
    Custom authentication backend that checks if user profile is active
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        # First, authenticate the user normally
        user = super().authenticate(request, username=username, password=password, **kwargs)
        
        if user is not None:
            # Check if user has a profile and if it's active
            try:
                profile = UserProfile.objects.get(user=user)
                if not profile.is_active:
                    # User exists but profile is inactive - deny authentication
                    return None
            except UserProfile.DoesNotExist:
                # User exists but has no profile - deny authentication
                return None
        
        return user
    
    def get_user(self, user_id):
        """
        Override get_user to also check if user profile is active
        """
        try:
            user = User.objects.get(pk=user_id)
            # Check if user profile is active
            try:
                profile = UserProfile.objects.get(user=user)
                if not profile.is_active:
                    return None
            except UserProfile.DoesNotExist:
                return None
            return user
        except User.DoesNotExist:
            return None
