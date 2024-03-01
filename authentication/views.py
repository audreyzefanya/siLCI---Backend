from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ParseError
from django.http import Http404
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserRegistrationSerializer, UserDetailSerializer

    

@api_view(["POST"])
def login(request):
    try:
        username = request.data["username"]
        password = request.data["password"]

        user=get_object_or_404(
            CustomUser,
            username=username
        )

        if not check_password(password, user.password):
            raise AuthenticationFailed()
        
    except KeyError:
        raise ParseError()
    
    except Http404:
        raise AuthenticationFailed()

    
    serializer = CustomUserSerializer(user)

    tokens = RefreshToken.for_user(user)
    print(tokens)

    return Response(
        data={
            "access_token": str(tokens.access_token),
            "refresh_token": str(tokens),
            "data": serializer.data,
            "detail": "Logged in"
        },
        status=status.HTTP_200_OK

    )

@api_view(['POST'])
def register(request):
    serializer = CustomUserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET', 'PUT'])
def detailUserById(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserDetailSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    


    


