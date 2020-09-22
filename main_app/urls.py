from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('rules/', views.about, name='rules'),
    path('add_game/', views.add_game, name='add_game'),
    path('setup_game', views.setup_game, name='setup_game'),
    path('events/<str:room_name>/', views.generate_board, name='generate_board'),
    path('game/<str:room_name>/', views.generate_board, name='generate_board'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/<int:user_id>/<int:profile_id>/add_photo/', views.add_photo, name='add_photo'), 
    path('profile/<int:user_id>/', views.profile, name='profile'), 
    path('rooms/<str:room_name>/', views.room, name='room'), 
]
