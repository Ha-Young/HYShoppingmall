from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = Order
        fields = "__all__"