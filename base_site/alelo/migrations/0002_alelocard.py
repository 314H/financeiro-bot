# Generated by Django 2.2.8 on 2020-01-04 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alelo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AleloCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('last_numbers', models.CharField(max_length=4)),
            ],
        ),
    ]
