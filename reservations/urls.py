from django.urls import path
from . import views

urlpatterns = [
    path('', views.screening_list, name='screening_list'),
    path('screening/<int:pk>/', views.screening_detail, name='screening_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
]