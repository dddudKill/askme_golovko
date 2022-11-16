# Generated by Django 4.1.3 on 2022-11-12 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('text', models.TextField(verbose_name='Text')),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
    ]
