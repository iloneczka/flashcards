from django.db import models
from django.contrib.auth.models import User
import random


class Box(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    box_number = models.IntegerField()

    @staticmethod
    def get_users_boxes(user):
        boxes_with_cards = Box.objects.filter(user=user).values('box_number').distinct()
        return boxes_with_cards

    @staticmethod
    def create_new_box(user):
        max_box_number = Box.objects.filter(user=user).aggregate(models.Max('box_number'))['box_number__max']
        new_box_number = (max_box_number or 0) + 1
        Box.objects.create(user=user, box_number=new_box_number)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    RATING_CHOICES = (
        ('happy', '🙂'),
        ('neutral', '😐'),
        ('sad', '🙁'),
    )
    user_rating = models.CharField(
        choices=RATING_CHOICES,
        default='neutral',
        max_length=10,
    )

    def __str__(self):
        return self.question

    def update_rating(self, rating):
        if rating in ['happy', 'neutral', 'sad']:
            self.user_rating = rating
            self.save()

    def get_random_card_based_on_rating(self):
        rating_choices = self.RATING_CHOICES
        weights = {
            'happy': 0.1,
            'neutral': 0.5,
            'sad': 0.9
        }
        cards_to_choose = []
        for choice, weight in rating_choices:
            cards_to_choose.extend([choice] * int(weights[choice] * 1000))
        selected_choice = random.choice(cards_to_choose)

        selected_card = Card.objects.filter(user_rating=selected_choice, user=self.user).order_by('?').first()

        return selected_card
