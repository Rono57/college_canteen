# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CategoryViewSet, MenuViewSet, SideDishViewSet,
    StockViewSet, OrderViewSet, ComplaintViewSet, RegisterView, CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'side-dishes', SideDishViewSet)
router.register(r'stock', StockViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'complaints', ComplaintViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]