from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'cards', views.CardView, basename='card')
router.register(r'boxes', views.BoxView, basename='box')

urlpatterns = [
    path('', views.home, name="home"),
    path('all_cards/<int:box_number>/', views.all_cards, name="all_cards"),
    path('user_panel/', views.user_panel, name="user_panel"),
    path('create_new_card.html', views.create_new_card, name="create_new_card"),
    path('export_cards/', views.export_cards, name='export_cards'),
    path('delete_card/<int:card_id>/', views.delete_card, name="delete_card"),
    path('edit_card/<int:card_id>/', views.edit_card, name='edit_card'),
    path('move_card/<int:card_id>/', views.move_card, name='move_card'),
    path('export_to_excel/', views.export_to_excel, name='export_to_excel'),
    path('export_to_csv/', views.export_to_csv, name='export_to_csv'),
    path('export_to_pdf/', views.export_to_pdf, name='export_to_pdf'),
    path('print_table/', views.print_table, name='print_table'),
    path('flashcards/<str:box_number>/', views.flashcard_program, name='flashcard_program'),
    path('update_rating_and_get_new_card/', views.update_rating_and_get_new_card, name='update_rating_and_get_new_card'),
    # path('registration/login/', views.user_login, name='login'),
    path('registration/signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('create_new_box/', views.create_new_box, name='create_new_box'),
    path('delete_box/<int:box_number>/', views.delete_box, name='delete_box'),
    path('get_available_boxes/', views.get_available_boxes, name='get_available_boxes'),
    path('api/', include(router.urls)),
    path('user/', views.user_profile, name='user_profile'),
    path('generate_token/', views.generate_token, name='generate_token'),
    path('change_username/', views.change_username, name='change_username'),
]
