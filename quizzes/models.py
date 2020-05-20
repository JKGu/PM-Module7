from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from django.utils import timezone
from django.dispatch import receiver

from django.db.models.signals import post_save,pre_save,post_delete


class Quizzes(models.Model):
    quiz_title = models.CharField(max_length=50)
    quiz_description = models.CharField(max_length=50)
    quiz_difficulty = models.IntegerField()
    scores = JSONField()
    def __str__(self):
        return self.quiz_title

class Question(models.Model):
    question_title = models.CharField(max_length=50)
    question_text = models.CharField(max_length=100)
    is_multi_answer = models.BooleanField()
    quiz_foreign_key = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    def __str__(self):
        return self.question_title

class Answer(models.Model):
    answer_title = models.CharField(max_length=50)
    answer_text = models.CharField(max_length=100)
    is_correct_answer = models.BooleanField()
    number_of_points = models.IntegerField()
    question_foreign_key = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return self.answer_title

def update_question(sender, instance, **kwargs):
    question = instance.question_foreign_key
    if len(list(question.answer_set.all().filter(is_correct_answer=True)))>1:
        question.is_multi_answer = True
        question.save()

def update_question_after_deletion(sender, instance, **kwargs):
    question = instance.question_foreign_key

    if len(list(question.answer_set.all().filter(is_correct_answer=True)))<=1:
        question.is_multi_answer = False
        question.save()

def remove_score(sender, instance, **kwargs):
    pk = instance.pk

    for quiz in Quizzes.objects.all():
        data = quiz.scores
        if str(pk) in data:
            del data[str(pk)]

        quiz.scores = data
        quiz.save()

post_save.connect(update_question, sender=Answer)
post_delete.connect(update_question_after_deletion,sender=Answer)
post_delete.connect(remove_score,sender=User)
