from rest_framework import serializers
from .models import ShippingRouteQuery, RoutePoint


class RoutePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePoint
        fields = ['id', 'name', 'description', 'order', 'point_type', 'country', 'city']


class ShippingRouteQuerySerializer(serializers.ModelSerializer):
    route_points = RoutePointSerializer(many=True, read_only=True)

    class Meta:
        model = ShippingRouteQuery
        fields = ['id', 'created_at', 'origin_country', 'destination_country',
                  'product_name', 'transport_method', 'route_points']
        read_only_fields = ['id', 'created_at', 'route_points', 'transport_method']


class ShippingRouteRequestSerializer(serializers.Serializer):
    origin_country = serializers.CharField(max_length=100)
    destination_country = serializers.CharField(max_length=100)
    product_name = serializers.CharField(max_length=200)
