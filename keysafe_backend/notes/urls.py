from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),

    path('notes/add/', add_note_view, name='add-note'),
    path('notes/<int:pk>/', note_detail_view, name='note-detail'),
    path('notes/<int:pk>/edit/', edit_note_view, name='edit-note'),
    path('notes/<int:pk>/delete/', delete_note_view, name='delete-note'),
]