# Generated by Django 5.1 on 2024-09-30 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_alter_tableofcontent_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='highResCover',
            field=models.ImageField(blank=True, null=True, upload_to='publication_images'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='image',
            field=models.ImageField(upload_to='publication_images'),
        ),
    ]