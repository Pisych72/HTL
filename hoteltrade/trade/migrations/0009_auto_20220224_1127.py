# Generated by Django 3.1.13 on 2022-02-24 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0008_auto_20220224_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='dealer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='trade.saler', verbose_name='Поставщик'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='doc',
            name='typedoc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trade.typedoc', verbose_name='Тип документа'),
        ),
    ]
