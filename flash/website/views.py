from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView)
from website.models import Card
import random

def home(request):
    all_cards = Card.objects.all()
    random_card = random.choice(all_cards)
    return render(request, 'home.html', {'card': random_card})

def all_cards(request):
    all_cards = Card.objects.all()
    print(all_cards)  # Dodaj ten wiersz
    return render(request, 'all_cards.html', {'all_cards': all_cards})


def create_new_card(request):
    if request.method == "POST":
        answer = request.POST['answer']
        question = request.POST['question']
        box= request.POST['box']
        card = Card(question=question, answer=answer, box=box)
        card.save()
        return render(request, 'create_new_card.html', {'added': True, 'question': question, 'answer': answer, 'box':box})
    return render(request, 'create_new_card.html', {'added': False})

    # return render(request, 'create_new_card.html', {})


def export_cards(request):
    return render(request, 'export_cards.html', {})


# class CardListView(ListView):
#         model = Card
#         queryset = Card.objects.all().order_by("box", "-date_created")

# class CardUpdateView(CreateView, UpdateView):
#     success_url = reverse_lazy("card-list")
