# Generated by Django 4.0 on 2022-02-13 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_profile_email_alter_profile_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='profile_pictures/default_profile_picture.png', max_length=255, upload_to='profile_pictures/'),
        ),
    ]
