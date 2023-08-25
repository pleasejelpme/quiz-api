from rest_framework import serializers
from quizes.models import Quiz, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(read_only=True, source='answer_set', many=True)
    class Meta: 
        model = Question
        fields = '__all__'


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(read_only=True, source='question_set', many=True)

    class Meta:
        model = Quiz
        fields = '__all__'


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        extra_kwargs = {
            'created': {'read_only': True},
            'times_completed': {'read_only': True},
            'creator': {'read_only': True}
        }


    def validate_required_score(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError('Score percentage must be between 1 and 100')
        return value
    