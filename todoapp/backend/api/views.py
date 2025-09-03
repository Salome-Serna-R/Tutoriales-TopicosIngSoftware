from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import permissions, generics
from .serializers import ToDoSerializer, ToDoToggleCompleteSerializer
from todo.models import ToDo

from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class ToDoListCreate(generics.ListCreateAPIView):
    # List APIView requires two mandatory attributes, serializer_class and queryset
    # We specify ToDoSerializer which we have earlier implemented

    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user).order_by("-created")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ToDoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)
    

class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = ToDoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.instance.completed = not serializer.instance.completed
        serializer.save()


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                username=data["username"], password=data["password"]
            )
            token = Token.objects.create(user=user)
            return JsonResponse({"token": str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(
                {"error": "username taken. choose another username"}, status=400
            )
    return JsonResponse({"detail": "Method not allowed"}, status=405)


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        user = authenticate(
            request, username=data.get("username"), password=data.get("password")
        )
        if user is None:
            return JsonResponse(
                {"error": "unable to login. check username and password"}, status=400
            )
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({"token": str(token)}, status=200)
    return JsonResponse({"detail": "Method not allowed"}, status=405)