# Generated by Django 2.2.7 on 2019-12-28 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managesystem', '0005_auto_20191228_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='back_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='year',
            field=models.IntegerField(),
        ),
    ]