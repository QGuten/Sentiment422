# Generated by Django 3.2 on 2021-04-27 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_auto_20210427_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorinfo',
            name='creator_gender',
            field=models.CharField(default='f', max_length=64, null=True, verbose_name='用户性别'),
        ),
    ]