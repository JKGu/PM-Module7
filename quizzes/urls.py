from django.urls import path

from . import views

app_name = 'quizzes'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:quiz_id>/', views.detail, name='detail'),
    path('<int:quiz_id>/<int:question_id>/',
         views.detail_question, name="detail_question"),
    path('<int:quiz_id>/<int:question_id>/<int:answer_id>',
         views.detail_answer, name="detail_answer"),
    path('delete/<int:quiz_id>', views.delete, name='delete'),
    path('delete-answer/<int:answer_id>', views.delete_answer, name='delete_answer'),
    path('delete-question/<int:question_id>', views.delete_question, name='delete_question'),
    path('create/', views.create, name='create'),
    path('create-question/', views.create_question, name='create_question'),
    path('create-answer/', views.create_answer, name='create_answer'),
    path('taker_index/', views.taker_index, name='taker_index'),
    path('admin_index/', views.admin_index, name='admin_index'),

    path('taker_detail/<int:id>/',views.taker_detail,name='taker_detail'),





]
