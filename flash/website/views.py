from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from website.models import Card, BOXES
import random

def home(request):
    all_cards = Card.objects.all()
    random_card = random.choice(all_cards)
    return render(request, 'home.html', {'card': random_card})

def all_cards(request):
    all_cards = Card.objects.all()
    return render(request, 'all_cards.html', {'all_cards': all_cards})

import json

def edit_card(request, card_id):
    print("Wszedłem!!!!")
    card = get_object_or_404(Card, pk=card_id)

    if request.method == 'POST':
        print("Sprawdzam request", request.body)
        body_unicode = request.body.decode('utf-8')  # Decode byte string to unicode string
        body_data = json.loads(body_unicode)
        print('body_data', body_data)

        question = body_data.get('question')
        print('question', question)
        answer = body_data.get('answer')
        print(answer)
        box_value = body_data.get('box', 'box1') 

        # Map box value to box number
        box_mapping = {
            'box1': 1,
            'box2': 2,
            'box3': 3,
        }
        box = box_mapping.get(box_value, 1) 

        if question and answer and box in BOXES:
            card.question = question
            card.answer = answer
            card.box = box
            card.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})

    return render(request, 'edit_card.html', {'card': card})


def delete_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == 'POST':
        card.delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}) 

def create_new_card(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        box_value = request.POST.get('box', 'box1') 

        # Map box value to box number
        box_mapping = {
            'box1': 1,
            'box2': 2,
            'box3': 3,
        }
        box = box_mapping.get(box_value, 1) 

        if question and answer and box in BOXES:
            card = Card.objects.create(question=question, answer=answer, box=box)
            added = True  # A flag to indicate that a new card was added
            return render(request, 'create_new_card.html', {'added': added, 'question': question, 'answer': answer})

    return render(request, 'create_new_card.html')

def export_cards(request):
    unique_boxes = Card.objects.values('box').distinct()
    all_cards = Card.objects.all()
    context = {'unique_boxes': unique_boxes, 'all_cards': all_cards}
    return render(request, 'export_cards.html', context)

