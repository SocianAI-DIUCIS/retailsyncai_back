from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    sku = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.FloatField(required=True)
    category = serializers.CharField(required=False, allow_blank=True)
    in_stock = serializers.BooleanField(default=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
