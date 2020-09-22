from django.urls import path, include
from django.conf.urls import url
from . import views
import django_eventstream

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('rules/', views.rules, name='rules'),
    path('add_game/', views.add_game, name='add_game'),
    path('setup_game', views.setup_game, name='setup_game'),
    path('events/<str:room_name>/', views.generate_board, name='generate_board'),
    #url(r'^events/(?P<channel>\w+)/', include(django_eventstream.urls), {'format-channels': ['{channel}']}),
    path('game/<str:room_name>/', views.generate_board, name='generate_board'),
    path('game/<str:room_name>/actions', views.generate_actions, name='generate_actions'),
    path('game/<str:room_name>/next', views.push_next_stage, name='push_next_stage'),
    path('hand/rob/', views.hand_rob, name='hand_rob'),
    path('hand/<str:room_name>/vote/', views.hand_vote, name='hand_vote'),
    path('hand/<str:room_name>/voted/<int:voted_id>', views.hand_voted, name='hand_voted'),
    path('hand/<str:hand_id>/', views.hand_reveal, name='hand_reveal'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/<int:user_id>/<int:profile_id>/add_photo/', views.add_photo, name='add_photo'), 
    path('profile/<int:user_id>/', views.profile, name='profile'), 
    path('rooms/<str:room_name>/', views.room, name='room'), 
]

#With profile now created we will need to either redirect user to the profile upon signup and/or have a button on the navbar for user. I advocate for both.

#need to add forms to templates