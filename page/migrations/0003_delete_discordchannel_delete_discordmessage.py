# Generated by Django 5.0.6 on 2024-05-31 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_discordchannel_discordmessage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DiscordChannel',
        ),
        migrations.DeleteModel(
            name='DiscordMessage',
        ),
    ]
