from django.urls import path
from . import views

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
    path('add_game', views.add_game, name='add_game'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profilepic/<user_id>/add_photo/', views.add_photo, name='add_photo'), #added for AWS profiles, referencing profile class SVL
    path('profile/<user_id>', views.profile, name='profile'), #where the profile shall live SVL
    path('rooms/<str:room_name>/', views.room, name='room'), #from changes in merge
]

#With profile now created we will need to either redirect user to the profile upon signup and/or have a button on the navbar for user. I advocate for both.

#need to add forms to templates