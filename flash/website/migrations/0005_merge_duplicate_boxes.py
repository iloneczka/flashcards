from django.db import migrations, models
from django.db.models import Count
from django.conf import settings


def merge_duplicate_boxes(apps, schema_editor):
    Box = apps.get_model('website', 'Box')
    Card = apps.get_model('website', 'Card')

    duplicate_boxes = Box.objects.values('user', 'box_number').annotate(num_boxes=Count('id')).filter(num_boxes__gt=1)

    for box_info in duplicate_boxes:
        user_id = box_info['user']
        box_number = box_info['box_number']

        cards_to_move = Card.objects.filter(box__user__id=user_id, box__box_number=box_number)

        if cards_to_move.exists():
            target_box = Box.objects.filter(user__id=user_id, box_number=box_number).first()

            for card in cards_to_move:
                card.box = target_box
                card.save()

            boxes_to_delete = Box.objects.filter(user__id=user_id, box_number=box_number).exclude(id=target_box.id)
            boxes_to_delete.delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0004_fix_empty_boxes'),
    ]

    operations = [
        migrations.RunPython(merge_duplicate_boxes),
    ]
