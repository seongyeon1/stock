from django.contrib import admin
from .models import Ticker

class TickerAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name')

admin.site.register(Ticker, TickerAdmin)