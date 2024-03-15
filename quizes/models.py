from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Quiz(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('hard', 'hard'),
    )

    title = models.CharField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    time_to_complete = models.PositiveIntegerField(
        help_text='duration of the quiz in minutes')
    required_score = models.PositiveIntegerField(
        help_text='required score to pass in %')
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    times_completed = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.quiestion_set.all()


class Question(models.Model):
    question = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.question[:50]

    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f'question: {self.question.question} | answer: {self.answer} | correct: {self.correct}'


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f'quiz: {self.quiz} | user: {self.user} | score: {self.score}'
