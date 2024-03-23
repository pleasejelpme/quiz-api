from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from quizes.models import Quiz, Question, Answer
from .permissions import IsCreatorOrReadOnlyPermission, IsAdminPermission
from .serializers import (
    QuizCreateSerializer,
    QuizListSerializer,
    QuestionSerializer,
    AnswerSerializer,
    QuizDetailSerializer)


class ListCreateQuizAPIView(ListCreateAPIView):
    queryset = Quiz.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuizCreateSerializer
        if self.request.method == 'GET':
            return QuizListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class DetailDeleteQuizAPIView(RetrieveDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = [IsCreatorOrReadOnlyPermission | IsAdminPermission]

    def get_queryset(self):
        return super().get_queryset()


class ListCreateQuestionAPIView(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ListCreateAnswerAPIView(ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
