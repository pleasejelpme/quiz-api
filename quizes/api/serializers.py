from rest_framework import serializers
from quizes.models import Quiz, Question, Answer

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            'title',
            'topic',
            'time_to_complete',
            'required_score',
            'difficulty',
        ]

    def validate_required_score(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError('Score percentage must be between 1 and 100')
        return value
    