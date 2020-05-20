from django.contrib import admin
from .models import Quizzes, Question, Answer

admin.site.register(Quizzes)
admin.site.register(Question)
admin.site.register(Answer)
# Register your models here.
