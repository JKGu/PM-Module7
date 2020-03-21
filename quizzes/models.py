from django.db import models


class Quiz(models.Model):
    quiz_title = models.CharField(max_length=50)
    quiz_description = models.CharField(max_length=50)
    quiz_difficulty = models.IntegerField()
    def __str__(self):
        return self.quiz_title

class Question(models.Model):
    question_title = models.CharField(max_length=50)
    question_text = models.CharField(max_length=100)
    is_multi_answer = models.BooleanField()
    quiz_foreign_key = models.ForeignKey(Quiz, on_delete=models.CASCADE)
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
