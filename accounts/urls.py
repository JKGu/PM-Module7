from django.urls import include, path
from . import views
from quizzes.views import index
urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('index',index, name='index'),
    path('update_role/<int:user_id>/',views.update_role, name='update_role'),

]
