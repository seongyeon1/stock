# Generated by Django 3.2.8 on 2021-10-29 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticker', '0001_initial'),
        ('news', '0002_news_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='ticker',
        ),
        migrations.AddField(
            model_name='news',
            name='ticker',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ticker.ticker', verbose_name='종목명'),
        ),
    ]