# encoding: utf-8
from apps.tasks_api.serializer import TaskSerializer
from apps.tasks_api.models import Task
from django.db import transaction
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


class TaskViewSet(viewsets.GenericViewSet):
    """List all task snippets."""
    serializer_class = TaskSerializer
    # lookup_fields = ["id", "title", "description"]

    def get_queryset(self):
        tasks = Task.objects.all()
        return tasks

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}

        pk_field = self.lookup_field
        if self.kwargs[pk_field]:
            filter[pk_field] = self.kwargs[pk_field]

        obj = get_object_or_404(queryset, **filter)
        return obj

    def retrieve(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            serializer = self.get_serializer(task)
        except Http404 as exc:
            return Response(data=exc.args[0], status=status.HTTP_404_NOT_FOUND)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """Get a list of tasks."""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
        except Http404 as exc:
            return Response(data=exc.args[0], status=status.HTTP_404_NOT_FOUND)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Creates a new Task."""
        serializer_data = request.data
        serializer = self.get_serializer(data=serializer_data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as exc:
            return Response(data=exc.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        """"""
        partial = kwargs.pop("partial", False)
        serializer_data = request.data

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=serializer_data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Http404 as exc:
            return Response(data=exc.args[0], status=status.HTTP_404_NOT_FOUND)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic()
    def partial_update(self, request, *args, **kwargs):
        """Partially updates a Task."""
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        """"""
        try:
            task = self.get_object()
            task.delete()
        except Exception as exc:
            return Response(data=exc.args[0], status=status.HTTP_400_BAD_REQUEST)

        return Response(data="Task {} successfully deleted!".format(task.title), status=status.HTTP_204_NO_CONTENT)
