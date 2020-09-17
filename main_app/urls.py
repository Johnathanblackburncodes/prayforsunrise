from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_game', views.add_game, name='add_game'),
    path('setup_game', views.setup_game, name='setup_game'),
    path('accounts/signup/', views.signup, name='signup'),
    path('rooms/<str:room_name>/', views.room, name='room'),
]
