from django.db import models

class Booking(models.Model):
    email = models.EmailField()
    travel_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.email} - {self.travel_date}"
