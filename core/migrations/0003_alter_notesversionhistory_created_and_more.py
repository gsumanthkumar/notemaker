# Generated by Django 5.0.2 on 2024-02-20 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_notesversionhistory_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notesversionhistory',
            name='created',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='notesversionhistory',
            name='deleted',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='notesversionhistory',
            name='updated',
            field=models.BooleanField(null=True),
        ),
    ]