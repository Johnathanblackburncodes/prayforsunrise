from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/<str:room_name>/', views.room, name='room'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profilepic/<int:profile_id>/add_photo/', views.add_photo, name='add_photo'), #added for AWS profiles, referencing profile class SVL
]
