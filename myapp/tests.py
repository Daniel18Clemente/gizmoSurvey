from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from .models import UserProfile, Section


class ActiveUserAuthenticationTest(TestCase):
    """Test cases for active user authentication"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test users
        self.active_user = User.objects.create_user(
            username='active_user',
            password='testpass123',
            first_name='Active',
            last_name='User'
        )
        
        self.inactive_user = User.objects.create_user(
            username='inactive_user',
            password='testpass123',
            first_name='Inactive',
            last_name='User'
        )
        
        # Create test section
        self.section = Section.objects.create(
            name='Test Section',
            code='TEST001',
            description='Test section for testing'
        )
        
        # Create user profiles
        self.active_profile = UserProfile.objects.create(
            user=self.active_user,
            role='student',
            section=self.section,
            is_active=True
        )
        
        self.inactive_profile = UserProfile.objects.create(
            user=self.inactive_user,
            role='student',
            section=self.section,
            is_active=False
        )
    
    def test_active_user_can_login(self):
        """Test that active users can login successfully"""
        response = self.client.post('/login/', {
            'username': 'active_user',
            'password': 'testpass123'
        })
        
        # Should redirect to student dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/student/')
    
    def test_inactive_user_cannot_login(self):
        """Test that inactive users cannot login"""
        response = self.client.post('/login/', {
            'username': 'inactive_user',
            'password': 'testpass123'
        })
        
        # Should stay on login page with error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your account has been deactivated')
    
    def test_inactive_user_logged_out_on_page_access(self):
        """Test that inactive users are logged out when accessing pages"""
        # First login the inactive user (bypassing our checks)
        self.client.force_login(self.inactive_user)
        
        # Try to access a protected page
        response = self.client.get('/student/')
        
        # Should be redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/student/')
    
    def test_user_without_profile_cannot_login(self):
        """Test that users without profiles cannot login"""
        # Create a user without a profile
        user_no_profile = User.objects.create_user(
            username='no_profile_user',
            password='testpass123'
        )
        
        response = self.client.post('/login/', {
            'username': 'no_profile_user',
            'password': 'testpass123'
        })
        
        # Should stay on login page with error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User profile not found')
    
    def test_active_user_can_access_dashboard(self):
        """Test that active users can access their dashboard"""
        self.client.login(username='active_user', password='testpass123')
        
        response = self.client.get('/student/')
        self.assertEqual(response.status_code, 200)
    
    def test_inactive_user_cannot_access_dashboard(self):
        """Test that inactive users cannot access dashboard even if logged in"""
        # Force login the inactive user
        self.client.force_login(self.inactive_user)
        
        response = self.client.get('/student/')
        
        # Should be redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/student/')
