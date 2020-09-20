from django.urls import path, include
from django.conf.urls import url
from . import views
import django_eventstream
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('rooms/<str:room_name>/', views.room, name='room'),
#     path('accounts/signup/', views.signup, name='signup'),
#     path('profilepic/<int:profile_id>/add_photo/', views.add_photo, name='add_photo'), #added for AWS profiles, referencing profile class SVL
#     path('profile/<int:profile_id>', views.profile, name='profile'), #where the profile shall live SVL
    
# ]

#testing USER case
urlpatterns = [
    path('', views.home, name='home'),
    path('add_game/', views.add_game, name='add_game'),
    path('setup_game', views.setup_game, name='setup_game'),
    path('events/<str:room_name>/', views.generate_board, name='generate_board'),
    #url(r'^events/(?P<channel>\w+)/', include(django_eventstream.urls), {'format-channels': ['{channel}']}),
    path('game/<str:room_name>/', views.generate_board, name='generate_board'),
    path('game/<str:room_name>/next', views.push_next_stage, name='push_next_stage'),
    path('hand/<str:hand_id>/', views.hand_reveal, name='hand_reveal'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profilepic/<int:user_id>/add_photo/', views.add_photo, name='add_photo'), #added for AWS profiles, referencing profile class SVL
    path('profile/<int:user_id>/', views.profile, name='profile'), #where the profile shall live SVL
    path('rooms/<str:room_name>/', views.room, name='room'), #from changes in merge
]

#With profile now created we will need to either redirect user to the profile upon signup and/or have a button on the navbar for user. I advocate for both.

#need to add forms to templates