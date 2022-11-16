# Generated by Django 4.1.3 on 2022-11-15 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='./user_avatars/avatar2.jpg', upload_to='./users_avatars'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='rating',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, max_length=6, related_name='questions', to='app.tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
