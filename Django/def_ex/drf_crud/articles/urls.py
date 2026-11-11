from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    path('comments/<int:comment_pk>/',views.comment_detail),
    path('comments/', views.comment_list),
    path('<int:article_pk>/comments/', views.comment_create),

]
