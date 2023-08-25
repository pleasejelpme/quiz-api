from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from quizes.models import Quiz, Question, Answer
from .serializers import (
    QuizListSerializer, 
    QuestionSerializer, 
    AnswerSerializer, 
    QuizDetailSerializer)

class ListCreateQuizAPIView(ListCreateAPIView):
    serializer_class = QuizListSerializer
    queryset = Quiz.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)



class DetailDeleteQuizAPIView(RetrieveDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer

    def get_queryset(self):
        return super().get_queryset()
 

class ListCreateQuestionAPIView(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ListCreateAnswerAPIView(ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer



