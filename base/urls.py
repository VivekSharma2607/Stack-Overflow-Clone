from django.urls import path
from . import views


app_name = 'base'

urlpatterns =[
    path('' , views.home , name="home"),
    path('about/' , views.about , name="about"),
    path('questions/' , views.QuestionListView.as_view() , name="question-list"),
    path('questions/new/' , views.QuestionCreateView.as_view() , name="question-create"),
    path('questions/<int:pk>' , views.QuestionDetailView.as_view() , name="question-detail"),
    path('questions/<int:pk>/update/' , views.QuestionUpdateView.as_view() , name="question-update"),
    path('questions/<int:pk>/delete' , views.QuestionDeleteView.as_view() , name="question-delete"),
    path('questions/<int:pk>/comment/' , views.AddCommentView.as_view() , name="question-comment"),
    path('like/<int:pk>' , views.like , name="like_post"),
]
