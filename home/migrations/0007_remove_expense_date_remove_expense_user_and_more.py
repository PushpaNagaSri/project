# Generated by Django 5.1.2 on 2024-11-13 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_expense_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='date',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='user',
        ),
        migrations.AlterField(
            model_name='expense',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='expense',
            name='reason',
            field=models.CharField(max_length=200),
        ),
    ]
