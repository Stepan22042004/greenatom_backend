# Generated by Django 3.2.3 on 2024-11-03 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0005_auto_20241101_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capacity',
            name='material',
            field=models.CharField(choices=[('Стекло', 'Стекло'), ('Биоотходы', 'Биоотходы'), ('Пластик', 'Пластик')], max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
