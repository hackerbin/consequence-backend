from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View


class PingAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Api to test authenticated route
        :param request:
        :return:
        """
        content = {'message': 'pong'}
        return Response(content)