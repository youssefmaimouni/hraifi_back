from rest_framework import viewsets, filters, status, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly

from .models import Category, Region, Artisan, Product, ContactMessage
from .serializers import (
    CategorySerializer, RegionSerializer,
    ArtisanSerializer, ProductSerializer,
    ContactMessageSerializer,
    ArtisanRegistrationSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset         = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class RegionViewSet(viewsets.ModelViewSet):
    queryset         = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAdminOrReadOnly]

class ArtisanViewSet(viewsets.ModelViewSet):
    queryset         = Artisan.objects.select_related('region')
    serializer_class = ArtisanSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['get'], url_path='products')
    def products(self, request, pk=None):
        """
        GET /api/artisans/{id}/products/
        List all products belonging to this artisan.
        """
        artisan = self.get_object()
        qs = artisan.products.select_related('category','region','artisan')
        page = self.paginate_queryset(qs)
        serializer = ProductSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset         = Product.objects.select_related('category', 'region', 'artisan')
    serializer_class = ProductSerializer
    filter_backends  = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category__id', 'region__id', 'artisan__id']
    search_fields    = ['name', 'description', 'materials', 'cultural_significance']
    permission_classes = [IsAuthenticatedOrReadOnly]

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset         = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

class ArtisanRegistrationView(generics.CreateAPIView):
    serializer_class   = ArtisanRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class ArtisanLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class ArtisanTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


# views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer