from django.urls import path
from .views import register_view, my_profile_view
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('profile/', my_profile_view, name='profile'),
    path('api/accounts/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/accounts/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
