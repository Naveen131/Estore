from rest_framework import serializers
from utils.common import CustomRetrieveUpdateAPIView

from product.models import Product, Order
from utils.common import CreateUpdateMixin

from product.models import Pizza

from product.models import PizzaOrder

from product.models import Toppings


class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer, CreateUpdateMixin):
    name = serializers.CharField(required=True, error_messages={'required': 'Name is required'})
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2,
                                     error_messages={'required': 'price is required'})
    stock = serializers.IntegerField(required=True, error_messages={'required': 'Name is required'})

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'stock',)


class OrderViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class OrderCreateSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = serializers.JSONField(required=True, error_messages={"required": "Products are required"})

    class Meta:
        model = Order
        fields = ('products',)

    def create(self, validated_data):
        products_data = validated_data.pop('products')  # Extract products from input
        total_price = 0
        product_details = []

        for product_entry in products_data:
            product_id = product_entry.get("id")
            quantity = product_entry.get("quantity")

            # Fetch the product
            product = Product.objects.get(id=product_id)

            # Check stock availability
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for product {product.name}. Available: {product.stock}, Requested: {quantity}."
                )

            # Deduct stock and calculate total price
            product.stock -= quantity
            product.save()
            total_price += product.price * quantity

            # Add serialized product details to the response
            product_details.append({
                "id": product.id,
                "name": product.name,
                "quantity": quantity,
                "price": product.price,
                "subtotal": product.price * quantity
            })

        # Create the order
        order = Order.objects.create(
                                     #user=validated_data['user'],
                                     total_price=total_price,
                                     products=product_details)

        return order

    def to_representation(self, instance):
        """Customize the serialized output of the order."""
        return {
            "id": instance.id,
            "user": instance.user.email,
            "products": instance.products,
            "total_price": instance.total_price,
            "status": instance.status
        }



class ToppingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toppings
        fields = '__all__'


class PizzaViewSerializer(serializers.ModelSerializer):
    toppings = ToppingsSerializer()
    class Meta:
        model = Pizza
        fields = "__all__"


class PizzaOrderViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaOrder
        fields = ('id', 'amount',)


class PizzaCreateSerializer(serializers.ModelSerializer):
    items = serializers.JSONField(required=True, error_messages={"required":"Items are Required"}, allow_null=False)

    class Meta:
        model = PizzaOrder
        fields = ('items',)


    def validate(self, attrs):
        items = attrs.get('items')

        for item in items:
            if item['quantity'] <= 0:
                raise serializers.ValidationError('Quantity should be greater than zero')
        return attrs

    def create(self, validated_data):
        items = validated_data.pop('items')
        amount = 0

        for item in items:
            pizza = Pizza.objects.get(id=item['id'])
            amount += pizza.price * item['quantity']

        order = PizzaOrder.objects.create(amount=amount, pizzas=items)

        return order

