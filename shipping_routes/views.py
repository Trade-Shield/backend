import json

from rest_framework import status, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ShippingRouteQuery, RoutePoint
from .serializers import ShippingRouteQuerySerializer, ShippingRouteRequestSerializer
from .services.gemini_service import GeminiService


class ShippingRouteViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    serializer_class = ShippingRouteQuerySerializer

    def get_queryset(self):
        return ShippingRouteQuery.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def analyze(self, request):  # analyze route
        serializer = ShippingRouteRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        origin = serializer.validated_data.get('origin_country')
        destination = serializer.validated_data.get('destination_country')
        product = serializer.validated_data.get('product_name')

        try:
            query = ShippingRouteQuery.objects.create(
                user=request.user,
                origin_country=origin,
                destination_country=destination,
                product_name=product
            )

            gemini_service = GeminiService()
            response_text = gemini_service.get_shipping_route_points(origin, destination, product)

            try:
                json_str = response_text

                if "```json" in response_text:
                    json_str = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    json_str = response_text.split("```")[1].split("```")[0].strip()

                route_data = json.loads(json_str)

                for i, point_data in enumerate(route_data.get('route_points', [])):
                    RoutePoint.objects.create(
                        shipping_query=query,
                        name=point_data.get('name', ''),
                        description=point_data.get('description', ''),
                        order=i
                    )

                return Response(
                    ShippingRouteQuerySerializer(query).data,
                    status=status.HTTP_201_CREATED
                )

            except json.JSONDecodeError as e:
                RoutePoint.objects.create(
                    shipping_query=query,
                    name="Raw Gemini Response",
                    description=response_text,
                    order=0
                )

                return Response({
                    'error': 'Failed to parse Gemini response',
                    'query_id': query.id,
                    'raw_response': response_text
                }, status=status.HTTP_206_PARTIAL_CONTENT)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
