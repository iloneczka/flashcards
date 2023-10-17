from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from website.models import Card, Box
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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
import pdfkit


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST' and 'create_box' in request.POST:
        new_box = Box.create_new_box(request.user)
        return JsonResponse({'status': 'success', 'new_box_number': new_box.box_number})

    if request.method == 'POST' and 'delete_box' in request.POST:
        box_id = request.POST.get('box_id')
        box = get_object_or_404(Box, pk=box_id, user=request.user)
        box.delete()
        return JsonResponse({'status': 'success'})

    unique_boxes = Box.get_unique_boxes(request.user)

    return render(request, 'home.html', {'unique_boxes': unique_boxes})


@login_required
def flashcard_program(request, box_number):
    unique_boxes = Box.get_unique_boxes(request.user)

    if request.method == 'POST':
        box_number = request.POST.get('box_number')

    if box_number == "0":
        random_card = Card.objects.filter(user=request.user).order_by('?').first()
    else:
        try:
            box_number = int(box_number)
            cards = Card.objects.filter(user=request.user, box__box_number=box_number)
            random_card = cards.first()
        except (ValueError, Card.DoesNotExist):
            random_card = None

    context = {
        'box_number': box_number,
        'random_card': random_card,
        'unique_boxes': unique_boxes,
        'no_cards': not random_card,
    }

    return render(request, 'flashcard_program.html', context)


def create_new_box(request):
    print("PRINTUJE 1 request:", request)
    if request.method == 'POST':
        print("PRINTUJE 2 request.method:", request.method)
        user = request.user

        max_box_number = Box.objects.filter(user=user).aggregate(models.Max('box_number'))['box_number__max']

        if max_box_number is not None:
            new_box_number = max_box_number + 1
        else:
            new_box_number = 1

        print('Drukuje max_box_number', max_box_number)
        print('Drukuje new_box_number', new_box_number)

        Box.objects.create(user=user, box_number=new_box_number)
        unique_boxes = Box.get_unique_boxes(request.user)

        return JsonResponse({'status': 'success', 'new_box_number': new_box_number, 'unique_boxes': list(unique_boxes)})
    return JsonResponse({'status': 'error'})


def delete_box(request, box_number):
    if request.method == 'POST':
        box = Box.objects.get(user=request.user, box_number=box_number)
        box.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@login_required
def all_cards(request, box_number=None):
    unique_boxes = Box.get_unique_boxes(request.user)

    if box_number is not None:
        box_number = int(box_number)  # Konwertuj na liczbę całkowitą

        if box_number != 0:
            cards = Card.objects.filter(user=request.user, box__box_number=box_number)
            context = {'cards': cards, 'unique_boxes': unique_boxes, 'box_number': box_number}
        else:
            cards = Card.objects.filter(user=request.user)
            context = {'cards': cards, 'unique_boxes': unique_boxes}
    else:
        context = {'unique_boxes': unique_boxes}

    return render(request, 'user_panel.html', context)


@login_required
def user_panel(request):
    unique_boxes = Box.get_unique_boxes(request.user)
    for box in unique_boxes:
        print(f"box: {box}")
        box['cards'] = Card.objects.filter(user=request.user, box__box_number=box.get('box_number'))
    # cards = Card.objects.filter(user=request.user)

    # context = {'cards': cards, 'unique_boxes': unique_boxes}
    # print(f"boxes hopefully with cards...: {unique_boxes}")
    context = {'unique_boxes': unique_boxes}
    print('context:', context)

    return render(request, 'user_panel.html', context)


def edit_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        question = body_data.get('question')
        answer = body_data.get('answer')

        if question and answer:
            card.question = question
            card.answer = answer
            card.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})

    return render(request, 'edit_card.html', {'card': card})


def move_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        new_box_number = body_data.get('box_number')

        # Sprawdź, czy nowy numer pudełka jest prawidłowy
        if new_box_number in Box.objects.filter(user=request.user).values_list('box_number', flat=True):
            card.box.box_number = new_box_number
            card.box.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})


def delete_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == 'POST':
        card.delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


@login_required
def create_new_card(request):
    unique_boxes = Box.objects.filter(user=request.user).values('box_number')

    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        box_number = request.POST.get('box')

        if question and answer and box_number:
            box = get_object_or_404(Box, user=request.user, box_number=box_number)
            new_card = Card.objects.create(user=request.user, question=question, answer=answer, box=box)
            added = True
            return render(request, 'create_new_card.html', {'added': added, 'new_card': new_card})
        else:
            return JsonResponse({'status': 'error'})

    return render(request, 'create_new_card.html', {'unique_boxes': unique_boxes})


def export_cards(request):
    unique_boxes = Box.get_unique_boxes(request.user)

    option = request.GET.get('option', None)

    if option is not None and option.isnumeric():
        box_number = int(option)
        cards = Card.objects.filter(user=request.user, box__box_number=box_number)
    else:
        cards = Card.objects.filter(user=request.user)

    context = {'cards': cards, 'unique_boxes': unique_boxes}
    return render(request, 'export_cards.html', context)


def export_to_excel(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')  # Zdekoduj
        body_data = json.loads(body_unicode)
        print('body_data', body_data)

        selected_box = body_data.get('selected_box')

        # Pobierz dane kart z wybranego boxa lub wszystkie karty
        if selected_box == 'all':
            all_cards = Card.objects.filter(user=request.user)
        else:
            all_cards = Card.objects.filter(box=selected_box, user=request.user)

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


def export_to_csv(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        print('body_data', body_data)

        selected_box = body_data.get('selected_box')

        # Pobierz dane kart z wybranego boxa lub wszystkie karty
        if selected_box == 'all':
            all_cards = Card.objects.filter(user=request.user)
        else:
            all_cards = Card.objects.filter(box=selected_box, user=request.user)

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
        selected_box = body_data.get('selected_box')

        all_cards = Card.objects.filter(user=request.user)

        if selected_box == 'all':
            all_cards = Card.objects.all()
        else:
            all_cards = Card.objects.filter(box=selected_box)

        context = {
            'all_cards': all_cards,
        }

        template = get_template('print_template.html')
        rendered_template = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="cards.pdf"'

        pdfkit.from_string(rendered_template, response)

        return response


def print_table(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        selected_box = body_data.get('selected_box')

        all_cards = Card.objects.filter(user=request.user)

        if selected_box == 'all':
            all_cards = Card.objects.all()
        else:
            all_cards = Card.objects.filter(box=selected_box)

        context = {
            'all_cards': all_cards,
        }

        template = get_template('print_template.html')
        rendered_template = template.render(context)  # Define rendered_template

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="cards.pdf"'

        pdfkit.from_string(rendered_template, response)

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


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                print('zalogowałem:', user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
