# Generated by Django 4.1.1 on 2023-01-03 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contatti', '0002_alter_aziende_altri_servizi_alter_aziende_google_map_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aziende',
            options={'ordering': ['archivio', 'nome']},
        ),
    ]
