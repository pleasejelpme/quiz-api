from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from quizes.models import Quiz


class CompletedQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

    def __str__(self):
        return f'user: {self.user.username} | quiz: {self.quiz} | score: {self.score}'


def update_quiz_times_completed(sender, instance, *args, **kwargs):
    if instance.score >= instance.quiz.required_score:
        instance.quiz.times_completed = instance.quiz.times_completed + 1
        instance.quiz.save()


post_save.connect(update_quiz_times_completed, sender=CompletedQuiz)
