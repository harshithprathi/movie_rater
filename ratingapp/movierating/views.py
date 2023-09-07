

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Movie, UserProfile, User
from .serializers import MovieSerializer, UserProfileSerializer, UserSerializer
from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from .models import Movie, UserProfile, User
from .serializers import MovieSerializer, UserProfileSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([])
def user_signup(request):
    """
    View for user registration (signup).
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.pk,
            'email': user.email,
            # 'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def user_login(request):
    """
    View for user login.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()
    if user and user.check_password(password):
        login(request, user)
        # token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            # 'token': token.key
        })
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    View for user logout.
    """
    request.auth.delete()
    logout(request)
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_profile(request):
    """
    View to retrieve the user's profile information.
    """
    user = request.user
    profile = UserProfile.objects.get(user=user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_user_profile(request):
    """
    View to edit the user's profile information.
    """
    user = request.user
    profile = UserProfile.objects.get(user=user)
    serializer = UserProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_review(request):
    """
    View to create a new review.
    """
    # print("requesdata",request.data)
    serializer = MovieSerializer(data=request.data)
    # print("requesdata", request.data)
    # print("validity", serializer.is_valid(), serializer)

    if serializer.is_valid():
        print("isvalid")
        # print("Save",serializer.save())
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_reviews(request):
    """
    View to retrieve reviews of the logged-in user.
    """
    # print("header", request.headers.get('user_id'))
    # user = request.user
    # print("user", user)
    reviews = Movie.objects.filter()
    serializer = MovieSerializer(reviews, many=True)
    # print("serializer.data", serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
def get_movie_reviews(request, movie_id):
    """
    View to retrieve reviews for a specific movie.
    """
    try:
        movie = Movie.objects.get(pk=movie_id)
        reviews = Movie.objects.filter(movie=movie)
        serializer = MovieSerializer(reviews, many=True)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response({'detail': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def edit_review(request, review_id):
    """
    View to edit a user's review.
    """
    try:
        review = Movie.objects.get(pk=review_id)
        if request.method == 'GET':
            serializer = MovieSerializer(review)
            return Response(serializer.data)
        elif request.method == 'PUT' and request.user == review.user:
            serializer = MovieSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    except Movie.DoesNotExist:
        return Response({'detail': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)


class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
