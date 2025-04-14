# api/serializers.py
from rest_framework import serializers
from core.models import User, Category, Menu, SideDish, Stock, Order, OrderDetail, OrderSideDish, Complaint, Payment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = user.user_type
        token['username'] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'place', 'user_type']
        read_only_fields = ['user_type']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'place']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data.get('phone', ''),
            place=validated_data.get('place', ''),
            user_type='student'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_active']

class SideDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = SideDish
        fields = ['id', 'name', 'price']

class MenuSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    side_dishes = SideDishSerializer(many=True, read_only=True)
    stock = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'category', 'name', 'description', 'price', 'is_available', 'side_dishes', 'stock']

    def get_stock(self, obj):
        stock = obj.stock.first()
        return stock.available_stock if stock else 0

class StockSerializer(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())

    class Meta:
        model = Stock
        fields = ['id', 'menu', 'available_stock', 'last_updated']

class OrderDetailSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(read_only=True)
    side_dishes = SideDishSerializer(many=True, read_only=True)

    class Meta:
        model = OrderDetail
        fields = ['id', 'menu', 'quantity', 'amount', 'side_dishes']

class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True, read_only=True)
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'student', 'total_amount', 'status', 'token_number', 'created_at', 'details', 'payment']

    def get_payment(self, obj):
        payment = obj.payment
        return {'status': payment.status, 'amount': payment.amount} if payment else None
        # api/serializers.py (add to OrderSerializer)
    def create(self, validated_data):
        order = Order.objects.create(
            student=self.context['request'].user,
            total_amount=0
        )
        total = 0
        # Example: Assume details are passed in request.data['details']
        for detail_data in self.context['request'].data.get('details', []):
            menu = Menu.objects.get(id=detail_data['menu_id'])
            quantity = detail_data['quantity']
            amount = menu.price * quantity
            detail = OrderDetail.objects.create(
                order=order,
                menu=menu,
                quantity=quantity,
                amount=amount
            )
            total += amount
            # Update stock
            stock = Stock.objects.get(menu=menu)
            if stock.available_stock < quantity:
                raise serializers.ValidationError(f"Not enough stock for {menu.name}")
            stock.available_stock -= quantity
            stock.save()
        order.total_amount = total
        order.save()
        Payment.objects.create(order=order, amount=total)
        return order

class ComplaintSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)

    class Meta:
        model = Complaint
        fields = ['id', 'student', 'description', 'reply', 'status', 'created_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'status', 'created_at']