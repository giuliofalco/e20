# Generated by Django 4.0.2 on 2022-02-25 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diario', '0008_alter_diario_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diario',
            name='note',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
