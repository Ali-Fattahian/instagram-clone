# Generated by Django 4.0 on 2022-02-15 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='profile_pictures/d_default_profile_picture_vpguse.png', max_length=255, upload_to='profile_pictures/'),
        ),
    ]
