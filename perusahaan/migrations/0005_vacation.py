# Generated by Django 3.0.3 on 2020-06-23 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perusahaan', '0004_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='vacation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.DateField()),
                ('end_day', models.DateField()),
                ('id_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='perusahaan.users')),
            ],
        ),
    ]
