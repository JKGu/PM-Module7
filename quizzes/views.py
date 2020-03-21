from django.shortcuts import render, get_object_or_404

from .models import Quiz
def index(request):
    quiz_list = Quiz.objects.order_by('quiz_title')
    context = {'quiz_list':quiz_list}
    return render(request, 'quizzes/index.html', context)

def detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quizzes/detail.html', {'quiz': quiz})
