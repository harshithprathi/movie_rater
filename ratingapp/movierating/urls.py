from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.MovieList.as_view(), name='movie-list'),
    path('login/', views.user_login, name='user-login'),
    path('signup/', views.user_signup, name='user-signup'),
    path('logout/', views.user_logout, name='user-logout'),
    path('reviews/', views.create_review, name='create_review'),
    path('user/reviews/', views.get_user_reviews, name='get_user_reviews'),
    path('movie/<int:movie_id>/reviews/',
         views.get_movie_reviews, name='get_movie_reviews'),
    path('review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('movies/', views.MovieList.as_view(), name='movie-list'),
    path('user/profile/', views.get_user_profile, name='get_user_profile'),
    path('user/profile/edit/', views.edit_user_profile, name='edit_user_profile'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
