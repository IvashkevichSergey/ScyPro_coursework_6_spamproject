from django.contrib import admin

from spam_messages.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
