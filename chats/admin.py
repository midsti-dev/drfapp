from django.contrib import admin

from chats.models import Message, Room

# Register your models here.

admin.site.register(Room)
admin.site.register(Message)
