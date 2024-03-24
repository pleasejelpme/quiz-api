from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.db import models

from django_rest_passwordreset.signals import reset_password_token_created

from quizes.models import Quiz


class CompletedQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE)
    max_score = models.PositiveIntegerField()
    times_completed = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'@{self.user.username} | {self.quiz} | max score: {self.max_score} | times completed: {self.times_completed}'

    class Meta:
        verbose_name = 'Competed Quiz'
        verbose_name_plural = 'Completed Quizes'


# Listens when a recovery token is created and sends it via email
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'recovery_password_url': reset_password_token.key
    }

    email_plaintext_message = render_to_string(
        'user_recover_password.txt', context)

    msg = EmailMultiAlternatives(
        # title
        'Password reset for Quizzing',

        # message
        email_plaintext_message,

        # from
        'pleasejelpmedev@outlook.com',

        # to
        [reset_password_token.user.email]
    )
    msg.send()
