from django.urls import path
from .views import ToDoListCreate, ToDoRetrieveUpdateDestroy, TodoToggleComplete, signup, login


urlpatterns = [
    path("todos/", ToDoListCreate.as_view(), name="todo-list"),
    path("todos/<int:pk>/", ToDoRetrieveUpdateDestroy.as_view()),
    path("todos/<int:pk>/toggle/", TodoToggleComplete.as_view()),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
]