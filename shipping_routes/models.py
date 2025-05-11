from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ShippingRouteQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_queries')
    created_at = models.DateTimeField(default=timezone.now)
    origin_country = models.CharField(max_length=100)
    destination_country = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)

    transport_method = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.origin_country} to {self.destination_country} - {self.product_name}"


class RoutePoint(models.Model):
    POINT_TYPES = (
        ('origin', 'Origin'),
        ('transit', 'Transit'),
        ('destination', 'Destination'),
    )

    shipping_query = models.ForeignKey(ShippingRouteQuery, on_delete=models.CASCADE, related_name='route_points')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    point_type = models.CharField(max_length=20, choices=POINT_TYPES, default='transit')
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
