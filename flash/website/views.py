from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from website.models import Card, BOXES
import random
import csv
import xlsxwriter
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def home(request):
    all_cards = Card.objects.all()
    random_card = random.choice(all_cards)
    return render(request, 'home.html', {'card': random_card})

def all_cards(request):
    all_cards = Card.objects.all()
    return render(request, 'all_cards.html', {'all_cards': all_cards})

import json

def edit_card(request, card_id):
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


def export_to_excel(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')  # Decode byte string to unicode string
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
        body_unicode = request.body.decode('utf-8')  # Decode byte string to unicode string
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
        body_unicode = request.body.decode('utf-8')  # Decode byte string to unicode string
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

         # Create the PDF document
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




       