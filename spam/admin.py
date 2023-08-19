from django.contrib import admin

from spam.models import Client, Message, Spam, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)


@admin.register(Spam)
class SpamAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'spam_time')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('spam', 'last_send', 'status')


