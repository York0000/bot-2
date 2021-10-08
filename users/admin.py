from django.contrib import admin

from users.models import TelegramUserModel


@admin.register(TelegramUserModel)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'username', 'first_name', 'last_name']
