from django.urls import path

from .views import (
    ListCreateQuizAPIView, 
    ListCreateQuestionAPIView, 
    DetailDeleteQuizAPIView,
    ListCreateAnswerAPIView)

urlpatterns = [
    path('quizes/', ListCreateQuizAPIView.as_view(), name='list-create-quiz'),
    path('quizes/<str:pk>', DetailDeleteQuizAPIView.as_view(), name='detail-quiz'),
    path('questions/', ListCreateQuestionAPIView.as_view(), name='list-create-question'),
    path('answers/', ListCreateAnswerAPIView.as_view(), name='list-create-answer')
]
