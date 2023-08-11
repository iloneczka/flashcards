from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def all_cards(request):
    return render(request, 'all_cards.html', {})

def create_new_card(request):
    return render(request, 'create_new_card.html', {})

def import_cards(request):
    return render(request, 'import_cards.html', {})
