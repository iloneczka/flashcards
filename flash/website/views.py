from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from website.models import Card, BOXES
import random
import csv
import xlsxwriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import json
import os
from pathlib import Path
from io import BytesIO
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, LoginForm


def home(request):
    return render(request, 'home.html')


def boxes(request):
    # all_cards = Card.objects.all()
    # random_card = random.choice(all_cards)
    unique_boxes = Card.objects.values('box').distinct()
    return render(request, 'boxes.html', {'unique_boxes': unique_boxes})


def flashcard_program(request, box_number):
    unique_boxes = Card.objects.values('box').distinct()

    if request.method == 'POST':
        box_number = request.POST.get('box_number')

    all_cards = Card.objects.all()

    if box_number == '0':
        cards = all_cards
    else:
        try:
            box_number = int(box_number)
            cards = all_cards.filter(box=box_number)
        except ValueError:
            cards = Card.objects.none()

    random_card = cards.order_by('?').first()

    context = {
        'box_number': box_number,
        'random_card': random_card,
        'all_cards': all_cards,
        'unique_boxes': unique_boxes,
        'all_cards': all_cards
    }

    if not cards.exists():
        context['no_cards'] = True

    return render(request, 'flashcard_program.html', context)


def all_cards(request, box_number):
    all_cards = Card.objects.all()
    unique_boxes = Card.objects.values('box').distinct()

    if box_number != 0:
        cards = all_cards.filter(box=box_number)
        context = {'cards': cards, 'unique_boxes': unique_boxes, 'box_number': box_number}
    else:
        context = {'cards': all_cards, 'unique_boxes': unique_boxes}

    return render(request, 'all_cards.html', context)


def edit_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)

    if request.method == 'POST':
        print("Sprawdzam request", request.body)
        body_unicode = request.body.decode('utf-8')  # Zdekoduj ten string, bez tego nie działało
        body_data = json.loads(body_unicode)
        print('body_data', body_data)

        question = body_data.get('question')
        print('question', question)
        answer = body_data.get('answer')
        print(answer)
        box_value = body_data.get('box', 'box1')

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
    unique_boxes = Card.objects.values('box').distinct()
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        box_value = request.POST.get('box', 'box1')

        box_mapping = {
            'box1': 1,
            'box2': 2,
            'box3': 3,
        }
        box = box_mapping.get(box_value, 1)

        if question and answer and box in BOXES:
            Card.objects.create(question=question, answer=answer, box=box)
            added = True
            return render(request, 'create_new_card.html', {'added': added, 'question': question, 'answer': answer, 'unique_boxes': unique_boxes})

    return render(request, 'create_new_card.html', {'unique_boxes': unique_boxes})


def export_to_excel(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')  # Zdekoduj
        body_data = json.loads(body_unicode)
        print('body_data', body_data)

        selected_box = body_data.get('selected_box')
        print(request.POST)
        print(selected_box)
        # Pobierz dane kart z wybranego boxa lub wszystkie karty
        if selected_box == 'all':
            all_cards = Card.objects.all()
        else:
            all_cards = Card.objects.filter(box=selected_box)

        # Tworzenie pliku Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=cards.xlsx'

        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Nagłówki kolumn
        header_format = workbook.add_format({'bold': True})
        worksheet.write(0, 0, 'Question', header_format)
        worksheet.write(0, 1, 'Answer', header_format)

        # Wprowadź dane
        row = 1
        for card in all_cards:
            worksheet.write(row, 0, card.question)
            worksheet.write(row, 1, card.answer)
            row += 1

        workbook.close()

        return response


def export_cards(request):
    unique_boxes = Card.objects.values('box').distinct()
    all_cards = Card.objects.all()

    context = {
        'unique_boxes': unique_boxes,
        'all_cards': all_cards,
    }

    return render(request, 'export_cards.html', context)


def export_to_csv(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        print('body_data', body_data)

        selected_box = body_data.get('selected_box')
        print(request.POST)
        print(selected_box)
        # Pobierz dane kart z wybranego boxa lub wszystkie karty
        if selected_box == 'all':
            all_cards = Card.objects.all()
        else:
            all_cards = Card.objects.filter(box=selected_box)

        # Tworzenie pliku CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=cards.csv'

        writer = csv.writer(response)
        writer.writerow(['Question', 'Answer'])  # Nagłówki kolumn

        for card in all_cards:
            writer.writerow([card.question, card.answer])

        return response


def export_to_pdf(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        print('body_data', body_data)

        selected_box = body_data.get('selected_box')
        print(request.POST)
        print(selected_box)
        # Pobierz dane kart z wybranego boxa lub wszystkie karty
        if selected_box == 'all':
            all_cards = Card.objects.all()
        else:
            all_cards = Card.objects.filter(box=selected_box)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cards.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        data = [[card.question, card.answer] for card in all_cards]

        # Create the table
        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 1), (-1, -1), 10),  # Adjust
            ('RIGHTPADDING', (0, 1), (-1, -1), 10),
            ('COLWIDTH', (0, 0), (-1, -1), 100),
        ])

        table.setStyle(style)

        elements = []
        elements.append(table)
        doc.build(elements)

        return response


def print_table(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        selected_box = body_data.get('selected_box')

        if selected_box == 'all':
            all_cards = Card.objects.all()
        else:
            all_cards = Card.objects.filter(box=selected_box)

        context = {
            'all_cards': all_cards,
        }

        template = get_template('print_template.html')
        template.render(context)

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Prepare the PDF content, such as a table, using reportlab
        elements = []
        elements.append(Table([['Card', 'Answer']] + [[card.question, card.answer] for card in all_cards]))
        doc.build(elements)

        # Set HTTP response headers
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cards.pdf"'

        # Save the PDF content to the HTTP response
        buffer.seek(0)
        response.write(buffer.read())

        return response


def update_rating_and_get_new_card(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            card_id = request.POST.get('card_id')  # Assuming you pass the card ID in the request data
            rating = request.POST.get('rating')  # Assuming you pass the rating in the request data

            card = Card.objects.get(id=card_id)

            # Update the card's rating
            card.update_rating(rating)

            # Get a new card based on the updated rating
            new_card = card.get_random_card_based_on_rating()

            # Prepare data to send back to the client
            response_data = {
                'question': new_card.question,
                'answer': new_card.answer,
            }

            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# signup page
def user_signup(request):
    print("drukuje")
    if request.method == 'POST':
        print('request:', request)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        print("Wszedlem tu else")
    return render(request, 'registration/signup.html', {'form': form})


# login page
def user_login(request):
    print('login druuuk')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
        else:
            form.add_error(None, "Both fields are required.")  # Dodajemy ogólny błąd do formularza
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


# logout page
def user_logout(request):
    logout(request)
    return redirect('registration/login.html')


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             # Obsługa błędnego logowania
#             pass

#     return render(request, 'flashcards/login.html')


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Automatyczne logowanie użytkownika po rejestracji
#             login(request, user)
#             return redirect('home')  # Przekierowanie po zalogowaniu
#     else:
#         form = UserCreationForm()

#     return render(request, 'flashcards/register.html', {'form': form})
