from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('all_cards.html', views.all_cards, name="all_cards"),
    # path('' ,views.CardListView.as_view(), name="all_cards"),
    path('create_new_card.html', views.create_new_card, name="create_new_card"),
    # path( "edit/<int:pk>", views.UpdateView.as_view(), name="card-update"),
    path('export_cards/', views.export_cards, name='export_cards'),
    path('delete_card/<int:card_id>/', views.delete_card, name="delete_card"),
    path('edit_card/<int:card_id>/', views.edit_card, name='edit_card'),
    path('export_to_excel/', views.export_to_excel, name='export_to_excel'),
    path('export_to_csv/', views.export_to_csv, name='export_to_csv'),
    path('export_to_pdf/', views.export_to_pdf, name='export_to_pdf')
    # path('print_table/', views.print_table, name='print_table'),
]