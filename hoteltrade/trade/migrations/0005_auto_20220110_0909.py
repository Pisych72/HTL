# Generated by Django 3.1.5 on 2022-01-10 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0004_good'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='photos', to='trade.category', verbose_name='Категория'),
        ),
    ]
