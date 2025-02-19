import datetime
from django.utils import timezone
from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer
from .tasks import send_email_task

# def send_email_task(email_address, message):
#     """Sends an email when the feedback form has been submitted."""
#     sleep(20)  # Simulate expensive operation(s) that freeze Django
#     # send_mail(
#     #     "Your Feedback",
#     #     f"\t{message}\n\nThank you!",
#     #     "support@example.com",
#     #     [email_address],
#     #     fail_silently=False,
#     # )
#     print("finished processing task", email_address, message)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        print("about to send email")
        email_message = f"Your travel have been booked for {booking}"
        send_email_task.apply_async(
            args=[booking.email, email_message]
        )
        # send_email_task(booking.email, email_message)