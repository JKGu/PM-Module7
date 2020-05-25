from django.shortcuts import render, get_object_or_404,reverse,redirect

import json
from django.http import HttpResponseRedirect

from .models import Quizzes, Question, Answer
from django.contrib.auth.models import Group,User
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def index(request):
    quiz_list = Quizzes.objects.order_by('quiz_title')
    print(quiz_list,"okokok")
    context = {'quiz_list':quiz_list}
    return render(request, 'quizzes/maker_index.html', context)

def detail(request, quiz_id): #detail of quiz
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    return render(request, 'quizzes/maker_detail.html', {'quiz': quiz})

def detail_question(request, quiz_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'quizzes/maker_answers.html', {'question': question})

def detail_answer(request, quiz_id, question_id, answer_id):
    return

def delete(request, quiz_id):
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
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

    quiz = Quizzes()
    quiz.quiz_title = quiz_title
    quiz.quiz_description = quiz_description
    quiz.quiz_difficulty = quiz_difficulty
    taker_ = Group.objects.get_or_create(name='quiz_taker')[0]
    data = {}
    for i in taker_.user_set.all():
        data[str(i.pk)] = {'score':'N/A','taken_on':''}

    quiz.scores = data
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
    question.quiz_foreign_key = Quizzes.objects.get(pk=quiz_id)
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
    quiz_list = Quizzes.objects.order_by('quiz_title')
    for i in quiz_list:
        data = i.scores
        if str(request.user.pk) in data.keys():
            pass
        else:
            data[str(request.user.pk)] = {'score':'N/A','taken_on':''}

        i.scores = data
        i.save()
    context = {'quiz_list':quiz_list}
    return render(request, 'quizzes/taker_index.html', context)
def taker_detail(request,id):
    quiz = get_object_or_404(Quizzes, pk=id)
    if request.method == "POST":
        data = request.POST
        points = 0
        question_ans_dict = {}
        for ques in quiz.question_set.all():
            question_ans_dict[ques.pk] = []

            ans_list = [Answer.objects.get(pk=int(i.split("_")[-1])) for i in data.getlist(f"question_{str(ques.pk)}")]
            correct_ans = list(ques.answer_set.all().filter(is_correct_answer=True))

            for ans in ans_list:
                question_ans_dict[ques.pk].append(ans.pk)
                points+=ans.number_of_points

            user_data = quiz.scores
            user_data[str(request.user.pk)] = {'score':points,'taken_on':timezone.now().strftime("%m/%d/%Y %I:%M:%S %p ")}

            quiz.scores = user_data
            quiz.save()

        return render(request, 'quizzes/quiz_taker_result.html', {'quiz':quiz,'user_info':question_ans_dict,'question_ans_dict':json.dumps(question_ans_dict),'points':points})
    return render(request, 'quizzes/quiz_taker_detail.html', {'quiz':quiz})

@login_required(login_url="login")
def admin_index(request):
    users = User.objects.all().order_by("username")
    return render(request, 'quizzes/admin_index.html',{'users':users})

def user_details(request,user_id):
    if 'quiz_admin' not in list(request.user.groups.all().values_list("name",flat=True)):
        return redirect("index")
    user = User.objects.get(pk=user_id)
    return render(request,"quizzes/user_details.html",{"user":user})


def delete_user(request,user_id):
    user = User.objects.get(pk=user_id)
    user.delete()

    return HttpResponseRedirect(reverse("quizzes:admin_index"))


def suspend_user(request,user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.save()

    return HttpResponseRedirect(reverse("quizzes:admin_index"))

def reinstate_user(request,user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()

    return HttpResponseRedirect(reverse("quizzes:admin_index"))
