from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'released_date')

admin.site.register(News, NewsAdmin)