import datetime
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Booking
from .serializers import BookingSerializer
from .tasks import send_email_task

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @swagger_auto_schema(
        request_body=BookingSerializer,
        responses={
            201: openapi.Response(description="Booking created successfully"),
            400: openapi.Response(description="Bad request"),
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new booking.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        booking = serializer.save()
        email_message = f"Your travel has been booked for {booking}"  # Improved message
        send_email_task.apply_async(args=[booking.email, email_message])


    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="List of all bookings")
        }
    )
    def list(self, request, *args, **kwargs):
        """
        List all bookings.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Retrieve a specific booking"),
            404: openapi.Response(description="Booking not found"),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific booking.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=BookingSerializer,
        responses={
            200: openapi.Response(description="Booking updated successfully"),
            400: openapi.Response(description="Bad request"),
            404: openapi.Response(description="Booking not found"),
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Update a booking.
        """
        reponse = super().update(request, *args, **kwargs)
        print(response)
        return response

    @swagger_auto_schema(
        responses={
            204: openapi.Response(description="Booking deleted successfully"),
            404: openapi.Response(description="No Booking matches the given query."),
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a booking.
        """
        return super().destroy(request, *args, **kwargs)


    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Test endpoint response")
        }
    )
    @action(detail=False, methods=['get'])  # Added a test endpoint
    def test(self, request):
        """
        A test endpoint.
        """
        data = {'message': 'This is a test endpoint'}
        return Response(data)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Documentation endpoint response")
        }
    )
    @action(detail=False, methods=['get'])  # Documentation endpoint (if needed)
    def documentation(self, request):
        """
        A documentation endpoint (example).  You might use a separate tool for this.
        """
        data = {'message': 'This is where your documentation would go'}
        return Response(data)