from django.urls import path
from . import views

urlpatterns = [
    path('', views.screening_list, name='screening_list'),
    path('screening/<int:pk>/', views.screening_detail, name='screening_detail'),
]