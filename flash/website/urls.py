from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('all_cards.html', views.all_cards, name="all_cards"),
    # path('' ,views.CardListView.as_view(), name="all_cards"),
    path('create_new_card.html', views.create_new_card, name="create_new_card"),
    path('export_cards.html', views.export_cards, name="export_cards"),
]
