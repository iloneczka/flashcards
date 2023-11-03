# Generated by Django 4.2.4 on 2023-09-27 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_boxes_for_existing_cards(apps, schema_editor):
    Card = apps.get_model('website', 'Card')
    Box = apps.get_model('website', 'Box')

    for card in Card.objects.all():
        # Tworzymy nowy obiekt Box
        box = Box.objects.create(user=card.user, box_number=card.box)
        print(f"Creating box based on previous data: {box}")

        # Ustawiamy box w Card
        # card.box = box
        # card.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box_number', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_boxes_for_existing_cards),
        migrations.AlterField(
            model_name='card',
            name='box',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.box'),
        ),
    ]
