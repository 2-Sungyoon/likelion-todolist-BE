from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    todo_id= serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Todo
        fields = [
            'todo_id',
            'user',
            'date',
            'content',
            'is_checked',
            'emoji',
        ]