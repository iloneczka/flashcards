from rest_framework import serializers
from .models import Card, Box

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'user', 'question', 'answer', 'box', 'date_created', 'user_rating')

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ('id', 'user', 'box_number')
        