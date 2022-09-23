from rest_framework import serializers
from apps.tasks_api.models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "completed", "created_at"]
