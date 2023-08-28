from django.contrib.auth.models import User
from django.db import models

from quizes.models import Quiz


class CompletedQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    
    def __str__(self):
        return f'user: {self.user.username} | quiz: {self.quiz} | score: {self.score}'

