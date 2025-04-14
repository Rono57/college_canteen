# canteen_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, register, login_view, logout_view, menu, orders, complaints
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('menu/', menu, name='menu'),
    path('orders/', orders, name='orders'),
    path('complaints/', complaints, name='complaints'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)