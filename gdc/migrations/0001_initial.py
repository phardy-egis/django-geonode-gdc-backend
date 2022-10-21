# Generated by Django 3.2.15 on 2022-10-13 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0084_remove_comments_from_actions'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicCategoryGDC',
            fields=[
                ('topiccategory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.topiccategory')),
                ('position_index', models.IntegerField(blank=True, null=True, verbose_name='Position index')),
                ('icon_img', models.FileField(blank=True, null=True, upload_to='', verbose_name='Image icon')),
            ],
            bases=('base.topiccategory',),
        ),
    ]