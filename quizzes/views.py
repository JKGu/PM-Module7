from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
import json
from django.http import HttpResponseRedirect

from .models import Quiz, Question, Answer

def index(request):
    quiz_list = Quiz.objects.order_by('quiz_title')
    context = {'quiz_list':quiz_list}
    return render(request, 'quizzes/index.html', context)

def detail(request, quiz_id): #detail of quiz
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quizzes/detail.html', {'quiz': quiz})

def detail_question(request, quiz_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'quizzes/answers.html', {'question': question})

def detail_answer(request, quiz_id, question_id, answer_id):
    return

def delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz.delete()
    return redirect('index')

def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def create(request):
    params_data = request.POST
    quiz_title = params_data['quiz_title']
    quiz_description = params_data['quiz_description']
    quiz_difficulty = params_data['quiz_difficulty']

    quiz = Quiz()
    quiz.quiz_title = quiz_title
    quiz.quiz_description = quiz_description
    quiz.quiz_difficulty = quiz_difficulty
    quiz.save()

    return redirect('index')

def create_question(request):
    params_data = request.POST
    quiz_id = int(params_data['quiz_id'])
    question_title = params_data['question_title']
    question_text = params_data['question_text']
    if 'is_multi' in params_data:
        is_multi = True
    else:
        is_multi = False
    question = Question()
    question.question_title = question_title
    question.question_text = question_text
    question.is_multi_answer = is_multi
    question.quiz_foreign_key = Quiz.objects.get(pk=quiz_id)
    question.save()
    return redirect('quizzes:detail', quiz_id=quiz_id)

def create_answer(request):
    params_data = request.POST
    question_id = int(params_data['question_id'])
    answer_title = params_data['answer_title']
    answer_text = params_data['answer_text']
    answer_point = params_data['answer_point']
    if 'is_correct' in params_data:
        is_correct = True
    else:
        is_correct = False
    answer = Answer()
    answer.answer_title = answer_title
    answer.answer_text = answer_text
    answer.is_correct_answer = is_correct
    answer.number_of_points = answer_point
    answer.question_foreign_key = Question.objects.get(pk=question_id)
    answer.save()
    return HttpResponseRedirect(params_data['next'])
    
def taker_index(request):
    quiz_list = Quiz.objects.order_by('quiz_title')
    context = {'quiz_list':quiz_list}
    return render(request, 'quizzes/taker_index.html', context)

def admin_index(request):
    return render(request, 'quizzes/admin_index.html')    