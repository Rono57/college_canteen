# api/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import User, Category, Menu, SideDish, Stock, Order, OrderDetail, OrderSideDish, Complaint, Payment
from .serializers import (
    UserSerializer, RegisterSerializer, CategorySerializer, MenuSerializer,
    SideDishSerializer, StockSerializer, OrderSerializer, ComplaintSerializer, PaymentSerializer,
    CustomTokenObtainPairSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class SideDishViewSet(viewsets.ModelViewSet):
    queryset = SideDish.objects.all()
    serializer_class = SideDishSerializer
    permission_classes = [permissions.IsAdminUser]

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAdminUser]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return Order.objects.all()
        return Order.objects.filter(student=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def pay(self, request, pk=None):
        order = self.get_object()
        if order.student != request.user and request.user.user_type != 'admin':
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        payment, created = Payment.objects.get_or_create(order=order, defaults={'amount': order.total_amount})
        payment.status = 'completed'
        payment.save()
        order.status = 'preparing'
        order.save()
        return Response({'status': 'Payment completed'})

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return Complaint.objects.all()
        return Complaint.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]