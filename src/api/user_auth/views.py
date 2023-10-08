from django.contrib.auth import login, authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from src.api.user_auth.serializers import *
from src.user_auth.models import UserProfile


class UserLoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSerializer(),
        responses={
            status.HTTP_200_OK: LoginResponseSerializer(),
        }
    )
    def post(self, request):
        """
        Login user.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }
                return Response(
                    LoginResponseSerializer(response_data).data,
                    status=status.HTTP_200_OK
                )
            return Response(
                {'error': 'Wrong credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserRegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            status.HTTP_201_CREATED: LoginResponseSerializer(),
        }
    )
    def post(self, request):
        """
        Register a new user.
        """
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()
                # Create an empty UserProfile for the created user
                UserProfile.objects.create(user=user)
            except:
                return Response({'name': 'Username already exist'}, status=status.HTTP_400_BAD_REQUEST)

            # Log in the user immediately upon successful registration
            login(request, user)

            # Generate and return an access token
            refresh = RefreshToken.for_user(user)
            response_data = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }

            # Return the response with the access token
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileGetUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve user profile.

        :param request: The HTTP request.
        :type request: rest_framework.request.Request

        :returns: The user profile.
        :rtype: rest_framework.response.Response

        """
        user = request.user  # Get the currently authenticated user
        serializer = UserProfileSerializer(user)
        data = serializer.data
        if 'avatar' in data and data['avatar']:
            data['avatar'] = request.build_absolute_uri(data['avatar'])

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserProfileSerializer,
        responses={
            status.HTTP_200_OK: UserProfileSerializer,
            status.HTTP_400_BAD_REQUEST: 'Validation error or bad request',
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Update user profile.

        :param request: The HTTP request.
        :type request: rest_framework.request.Request

        :returns: The updated user profile.
        :rtype: rest_framework.response.Response

        """
        user = request.user  # Get the currently authenticated user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            if 'avatar' in data and data['avatar']:
                data['avatar'] = request.build_absolute_uri(data['avatar'])
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
