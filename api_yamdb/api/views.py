from api.filters import TitleFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from reviews.models import Categories, Genres, Review, Title

from .permissions import AdminAccessOnly, ModerateAccessOrReadOnly, ReadOnly
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, GetTokenSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UsersMeSerializer, UsersSerializer)

User = get_user_model()


class RegistrationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user, _ = User.objects.get_or_create(
            **serializer.validated_data
        )
        code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения на сервисе YaMDB',
            f'Ваш код подтверждения: {code}',
            'noreplay@YaMDB.com',
            [serializer.validated_data['email']],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = GetTokenSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenresViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                    mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """
    Ресурс для предоставления модели Genres.
    """
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AdminAccessOnly | ReadOnly, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoriesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                        mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """
    Ресурс для предоставления модели Categories.
    """
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AdminAccessOnly | ReadOnly, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Ресурс для предоставления модели Title.
    """
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year',)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    permission_classes = [AdminAccessOnly | ReadOnly, ]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Ресурс для предоставления отзывов к Произведению.
    """
    serializer_class = ReviewSerializer
    permission_classes = [ModerateAccessOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Ресурс для предоставления комментариев к отзывам.
    """
    serializer_class = CommentsSerializer
    permission_classes = [ModerateAccessOrReadOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = [AdminAccessOnly]

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request, pk=None):
        user = request.user
        serializer = UsersMeSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
