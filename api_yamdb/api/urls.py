from django.urls import include, path
from rest_framework import routers

from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    GetTokenViewSet, RegistrationViewSet, ReviewViewSet,
                    TitlesViewSet, UsersViewSet)

v1_router = routers.DefaultRouter()


v1_router.register('users', UsersViewSet, basename='users')
v1_router.register('auth/signup', RegistrationViewSet, basename='v1_signup')
v1_router.register('auth/token', GetTokenViewSet, basename='v1_token')
v1_router.register(r'titles', TitlesViewSet, basename='titles')
v1_router.register(r'categories', CategoriesViewSet, basename='categories')
v1_router.register(r'genres', GenresViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
