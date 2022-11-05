import datetime
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.validators import UniqueValidator

from reviews.models import Genres, Categories, Title, Review, Comments

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            message = 'Вы не можете быть «me»'
            raise serializers.ValidationError(message)
        return value

    def validate(self, data):
        username = User.objects.filter(username=data['username'])
        email = User.objects.filter(email=data['email'])
        if username.intersection(email).exists():
            return data
        if username.exists():
            message = 'username already has been taken'
            raise serializers.ValidationError(message)
        if email.exists():
            message = 'email already has been taken'
            raise serializers.ValidationError(message)
        return data

    def create(self, validated_data):
        return validated_data


class GetTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', 'token')

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if default_token_generator.check_token(
                user, data['confirmation_code']):
            return data
        message = 'Invalid confirmation code'
        raise serializers.ValidationError(message)

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        token = AccessToken.for_user(user)
        return {'token': str(token)}


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'rating', 'description',
                  'year', 'category', 'genre')

    def get_rating(self, obj):
        title_id = obj.id
        rating = Review.objects.filter(
            title_id=title_id).aggregate(Avg('score'))
        if rating['score__avg']:
            return int(rating['score__avg'])
        return None


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'description',
                  'year', 'category', 'genre')

    def validate_year(self, value):
        year = datetime.datetime.today().year
        if value > year or value < 0:
            raise serializers.ValidationError("Please input correct year")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    score = serializers.IntegerField(required=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        value = int(value)
        if value < 1 or value > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        TITLE = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=TITLE, author=author).exists():
                raise serializers.ValidationError(
                    'Отзыв уже существует!Вы больше не можете добавлять отзыв')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comments
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.ChoiceField(choices=User.ROLES, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UsersMeSerializer(UsersSerializer):
    role = serializers.ChoiceField(choices=User.ROLES, read_only=True)
