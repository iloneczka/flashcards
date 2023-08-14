from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def all_cards(request):
    return render(request, 'all_cards.html', {})

def create_new_card(request):
    if request.method == "POST":
        answer = request.POST['answer']
        question = request.POST['question']
        print(f"XXXXX {answer}")
        return render(request, 'create_new_card.html', {'added': True, 'question': question, 'answer': answer})
    return render(request, 'create_new_card.html', {'added': False})

    # return render(request, 'create_new_card.html', {})


def import_cards(request):
    return render(request, 'import_cards.html', {})
