# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet, SpellingListViewSet, SpellingListWordViewSet, RegistrationView 
from rest_framework.authtoken.views import obtain_auth_token
from django.http import HttpResponse

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'spelling-lists', SpellingListViewSet, basename='spellinglist')
router.register(r'spelling-list-words',SpellingListWordViewSet ,basename='spellinglistword')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegistrationView.as_view(), name='register'),
]
