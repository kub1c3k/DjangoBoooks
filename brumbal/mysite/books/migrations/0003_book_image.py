# Generated by Django 5.1.2 on 2025-01-08 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_author_alter_book_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default=0, height_field='Null', upload_to='Null', width_field='Null'),
            preserve_default=False,
        ),
    ]
