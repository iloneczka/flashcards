from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .serializers import CardSerializer, BoxSerializer
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


class CardView(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()


class BoxView(viewsets.ModelViewSet):
    serializer_class = BoxSerializer
    queryset = Box.objects.all()


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

    users_boxes = Box.get_users_boxes(request.user)

    return render(request, 'home.html', {'users_boxes': users_boxes})


@login_required
def flashcard_program(request, box_number):
    users_boxes = Box.get_users_boxes(request.user)

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
        'users_boxes': users_boxes,
        'no_cards': not random_card,
    }

    return render(request, 'flashcard_program.html', context)


@login_required
def create_new_box(request):
    if request.method == 'POST':
        user = request.user

        max_box_number = Box.objects.filter(user=user).aggregate(models.Max('box_number'))['box_number__max']

        if max_box_number is not None:
            new_box_number = max_box_number + 1
        else:
            new_box_number = 1

        Box.objects.create(user=user, box_number=new_box_number)
        users_boxes = Box.get_users_boxes(request.user)

        return JsonResponse({'status': 'success', 'new_box_number': new_box_number, 'users_boxes': list(users_boxes)})
    return JsonResponse({'status': 'error'})


@login_required
def delete_box(request, box_number):
    if request.method == 'POST':
        box = Box.objects.get(user=request.user, box_number=box_number)
        box.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@login_required
def all_cards(request, box_number=None):
    users_boxes = Box.get_users_boxes(request.user)

    if box_number is not None:
        box_number = int(box_number)  # Konwertuj na liczbę całkowitą

        if box_number != 0:
            cards = Card.objects.filter(user=request.user, box__box_number=box_number)
            context = {'cards': cards, 'users_boxes': users_boxes, 'box_number': box_number}
        else:
            cards = Card.objects.filter(user=request.user)
            context = {'cards': cards, 'users_boxes': users_boxes}
    else:
        context = {'users_boxes': users_boxes}

    return render(request, 'user_panel.html', context)


@login_required
def user_panel(request):
    users_boxes = Box.get_users_boxes(request.user)
    for box in users_boxes:
        print(f"box: {box}")
        box['cards'] = Card.objects.filter(user=request.user, box__box_number=box.get('box_number'))
    # cards = Card.objects.filter(user=request.user)

    # context = {'cards': cards, 'users_boxes': users_boxes}
    # print(f"boxes hopefully with cards...: {users_boxes}")
    context = {'users_boxes': users_boxes}
    print('context:', context)

    return render(request, 'user_panel.html', context)


@login_required
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


@login_required
def move_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        new_box_number = body_data.get('box_number')
        print(request, "-request PRINTUJE")
        print(new_box_number, "-new_box_number PRINTUJE")

        user_boxes = Box.objects.filter(user=request.user)
        available_boxes = user_boxes.values_list('box_number', flat=True)
        print("available_boxes", list(available_boxes))
        print("warunek", int(new_box_number) in list(available_boxes))
        if int(new_box_number) in list(available_boxes):
            card.box = user_boxes.get(box_number=new_box_number)
            card.save()
            return JsonResponse({'status': 'success', 'available_boxes': list(available_boxes)})
        else:
            return JsonResponse({'status': 'error', 'available_boxes': list(available_boxes)})

    return JsonResponse({'status': 'error'})


@login_required
def get_available_boxes(request):
    user_boxes = Box.objects.filter(user=request.user)
    available_boxes = user_boxes.values_list('box_number', flat=True)
    return JsonResponse({'status': 'success', 'available_boxes': list(available_boxes)})


@login_required
def delete_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == 'POST':
        card.delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


@login_required
def create_new_card(request):
    users_boxes = Box.objects.filter(user=request.user).values('box_number')

    if not users_boxes:  # Jeśli users_boxes jest puste
        # Utwórz nowe pudełko
        new_box = Box.objects.create(user=request.user, box_number=1)  # Możesz ustawić odpowiedni numer pudełka
        box_number = new_box.box_number
        users_boxes = [{'box_number': box_number}]

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

    return render(request, 'create_new_card.html', {'users_boxes': users_boxes})


@login_required
def export_cards(request):
    users_boxes = Box.get_users_boxes(request.user)

    option = request.GET.get('option', None)

    if option is not None and option.isnumeric():
        box_number = int(option)
        cards = Card.objects.filter(user=request.user, box__box_number=box_number)
    else:
        cards = Card.objects.filter(user=request.user)

    context = {'cards': cards, 'users_boxes': users_boxes}
    return render(request, 'export_cards.html', context)


@login_required
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
            all_cards = Card.objects.filter(user=request.user, box__box_number=int(selected_box))

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


@login_required
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
            all_cards = Card.objects.filter(user=request.user, box__box_number=int(selected_box))

        # Tworzenie pliku CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=cards.csv'

        writer = csv.writer(response)
        writer.writerow(['Question', 'Answer'])  # Nagłówki kolumn

        for card in all_cards:
            writer.writerow([card.question, card.answer])

        return response


@login_required
def export_to_pdf(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')  # Decode byte string to unicode string
        body_data = json.loads(body_unicode)
        print('body_data', body_data)

        selected_box = body_data.get('selected_box')
        print(request.POST)
        print(selected_box)
        # Pobierz dane kart z wybranego boxa lub wszystkie karty
        if selected_box == 'all':
            all_cards = Card.objects.filter(user=request.user)
        else:
            all_cards = Card.objects.filter(user=request.user, box__box_number=int(selected_box))

        # Create the PDF document
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cards.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        data = [[card.question, card.answer] for card in all_cards]
        print(data)

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
            ('LEFTPADDING', (0, 1), (-1, -1), 10),  # Adjust left padding for data cells
            ('RIGHTPADDING', (0, 1), (-1, -1), 10),  # Adjust right padding for data cells
            ('COLWIDTH', (0, 0), (-1, -1), 100),  # Adjust column width for all columns
        ])

        table.setStyle(style)

        # Build the PDF
        elements = []
        elements.append(table)
        doc.build(elements)

        return response


@login_required
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


@login_required
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
