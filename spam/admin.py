from django.contrib import admin

from spam.models import Spam, Logs


@admin.register(Spam)
class SpamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'spam_time')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('spam', 'client', 'last_send', 'status')
