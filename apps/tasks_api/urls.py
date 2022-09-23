from django.urls import path
from apps.tasks_api import views as tasks_views


urlpatterns = [
    path("tasks/", tasks_views.TaskViewSet.as_view({"post": "create", "get": "list"}), name="task-add"),
    path("tasks/<int:pk>/", tasks_views.TaskViewSet.as_view(
        {"delete": "delete", "get": "retrieve", "patch": "partial_update", "put": "update"}
    ), name="task-detail"),
]
