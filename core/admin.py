from django.contrib import admin
from .models import UserProfile, Book, BookExchange

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(BookExchange)