from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ShippingRouteQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_queries')
    created_at = models.DateTimeField(default=timezone.now)
    origin_country = models.CharField(max_length=100)
    destination_country = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.origin_country} to {self.destination_country} - {self.product_name}"


class RoutePoint(models.Model):
    shipping_query = models.ForeignKey(ShippingRouteQuery, on_delete=models.CASCADE, related_name='route_points')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
