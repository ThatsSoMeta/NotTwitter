# Generated by Django 3.1.7 on 2021-03-05 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitteruser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitteruser',
            name='following',
        ),
    ]
