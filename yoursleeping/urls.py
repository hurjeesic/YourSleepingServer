from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data/list/', views.data_list, name='data_list'),
    path('data/add/', views.data_add, name='data_add'),
    path('data/delete/', views.data_delete, name='data_delete'),
    path('data/api/', views.ActivityList.as_view()),
    path('data/api/<int:pk>', views.ActivityDetail.as_view()),
]
