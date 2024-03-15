from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from quizes.models import Quiz


class CompletedQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE)
    max_score = models.PositiveIntegerField()
    times_completed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'@{self.user.username} | {self.quiz} | max score: {self.max_score} | times completed: {self.times_completed}'

    class Meta:
        verbose_name = 'Competed Quiz'
        verbose_name_plural = 'Completed Quizes'
