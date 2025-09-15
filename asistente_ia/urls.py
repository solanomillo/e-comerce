# asistente_ia/urls.py
from django.urls import path
from .views import chat_api

urlpatterns = [
    path("ask/", chat_api, name="chat_api"),
]
