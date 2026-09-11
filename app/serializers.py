from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from .models import Task, SubTask, Category
from django.contrib.auth.password_validation import validate_password


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']
        read_only_fields = ['owner']


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at', 'owner']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


    def create(self, validated_data):
        if Category.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError('Category with this name already exists!')
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if Category.objects.filter(name=validated_data['name']).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError('Category with this name already exists!')
        instance.name = validated_data['name']
        instance.save()
        return instance


class TaskDetailSerializer(serializers.ModelSerializer):
    subtask_set = SubTaskCreateSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Deadline date cannot be in the past!')
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Password does not match!')
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user