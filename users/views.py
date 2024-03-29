from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, NatureOfBusiness
from .serializers import RegisterSerializer, UserSerializer, BusinessSerializer, NatureOfBusinessSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        token, created = Token.objects.get_or_create(user=user)
        response = Response()
        response.set_cookie(key='Authorization', value='Token {}'.format(token), httponly=True)
        response.data = {'token': token.key}
        return response


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request.user.auth_token.delete()
        response = Response()
        response.delete_cookie(key='Authorization')
        response.data = {'message': 'logout successful'}
        return response


class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'user': UserSerializer(request.user).data})


class NatureOfBusinessesViews(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        nature_of_businesses = NatureOfBusiness.objects.all()
        serializer = NatureOfBusinessSerializer(nature_of_businesses, many=True)
        return Response(serializer.data)


class UserBusinessUpdate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = BusinessSerializer(data=request.data, context={
            'request': request
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
