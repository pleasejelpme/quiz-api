from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from quizes.models import Quiz, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer', 'correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False, source='answer_set')

    class Meta:
        model = Question
        fields = ['question', 'answers']


class QuizDetailSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(read_only=True, source='creator.username')
    questions = QuestionSerializer(
        read_only=True, source='question_set', many=True)

    class Meta:
        model = Quiz
        fields = '__all__'


class QuizCreateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set')

    class Meta:
        model = Quiz
        fields = [
            'title',
            'topic',
            'time_to_complete',
            'required_score',
            'difficulty',
            'questions'
        ]

        extra_kwargs = {
            'created': {'read_only': True},
            'times_completed': {'read_only': True},
            'creator': {'read_only': True}
        }

    def validate_required_score(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError(
                'Score percentage must be between 1 and 100')
        return value

    '''
    Overriding the create method so it can handle a 
    nested object in the POST request 
    '''

    def create(self, validated_data):
        print(validated_data)
        print('entered in create')
        questions_data = validated_data.pop('question_set')
        quiz = Quiz.objects.create(**validated_data)
        print('questions popped and quiz created')

        for single_question in questions_data:
            answers_data = single_question.pop('answer_set')
            question = Question.objects.create(quiz=quiz, **single_question)
            print('answers popped and question created')

            for single_answer in answers_data:
                print('created answer')
                Answer.objects.create(question=question, **single_answer)

        return quiz


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
