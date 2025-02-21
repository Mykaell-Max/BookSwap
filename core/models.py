from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile") # one to one relation, but u still have to use "User" to create a new user on the DB
    # and because of this, you should create a signal to this action (see core/signals.py)
    city = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class BookExchange(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests_made")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests_received")
    requested_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="requested_exchanges")
    offered_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="offered_exchanges")
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester} wants {self.requested_book}"
    

