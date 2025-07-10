from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, RegionViewSet,
    ArtisanViewSet, ProductViewSet,
    ContactMessageViewSet, ArtisanRegistrationView,
    ArtisanLoginView, ArtisanTokenRefreshView
)
from .views import CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet,     basename='category')
router.register(r'regions',    RegionViewSet,       basename='region')
router.register(r'artisans',   ArtisanViewSet,      basename='artisan')
router.register(r'products',   ProductViewSet,      basename='product')
router.register(r'contact',    ContactMessageViewSet, basename='contact')

urlpatterns = [
    path('api/auth/register/', ArtisanRegistrationView.as_view(), name='artisan-register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/',  ArtisanTokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]