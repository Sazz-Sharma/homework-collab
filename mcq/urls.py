from django.urls import path
from . import views

urlpatterns = [
    path("create_collection/", views.create_collection),
    path("get_collections/", views.get_collections),
    path("question_list/", views.question_list),
    path("create_question/", views.create_question),
    path("submit_answersheet/", views.submit_answersheet),
]