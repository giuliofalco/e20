# Generated by Django 4.1.1 on 2023-01-02 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aziende',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivio', models.CharField(blank=True, default='R', max_length=2, null=True)),
                ('categoria', models.CharField(max_length=150, null=True)),
                ('nome', models.CharField(max_length=250)),
                ('descrizione', models.TextField(blank=True, null=True)),
                ('indirizzo', models.CharField(max_length=300, null=True)),
                ('citta', models.CharField(blank=True, max_length=200, null=True)),
                ('cap', models.CharField(max_length=6, null=True)),
                ('provincia', models.CharField(blank=True, max_length=4, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('mail', models.EmailField(blank=True, max_length=200, null=True)),
                ('web', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('youtube', models.URLField(blank=True, null=True)),
                ('num_immagini', models.IntegerField(default=0)),
                ('servizi', models.CharField(blank=True, max_length=200, null=True)),
                ('altri_servizi', models.CharField(blank=True, max_length=300, null=True)),
                ('google_map', models.CharField(blank=True, max_length=300, null=True)),
                ('orari', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
    ]