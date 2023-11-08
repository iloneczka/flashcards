from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Count


def fix_migration_0003_errors(apps, schema_editor):
    Card = apps.get_model('website', 'Card')
    Box = apps.get_model('website', 'Box')
    print(Card, Box)

    empty_boxes = Box.objects.annotate(num_cards=Count('card')).filter(num_cards=0)

    for box in empty_boxes:
        box.delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0003_combine_cards_and_remove_empty_boxes'),
    ]

    operations = [
        migrations.RunPython(fix_migration_0003_errors),
    ]
