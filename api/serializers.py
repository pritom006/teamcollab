from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, ProjectMember, Task, Comment
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True,required=True)
    username = serializers.CharField(write_only=True,required=True)
    first_name = serializers.CharField(write_only=True,required=True)
    last_name = serializers.CharField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ['email','username', 'first_name', 'last_name' ,'password']

    def validate(self, attrs):
        user= User.objects.filter(email = attrs.get('email')).count()
        if user > 0:
            raise serializers.ValidationError({"email":"Please Add unique email"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password',]
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid Credentials")
        else:
            raise serializers.ValidationError("Both username and password are required")

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email',instance.email)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.save()
        return instance


class ProjectCrearteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True,required=False)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    owner= serializers.CharField(required=True)
    created_at = serializers.DateTimeField(read_only=True,required=False)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner','created_at']


    def create(self, validated_data):
        project = Project.objects.create(
            name = validated_data['name'],
            description = validated_data['description'],
            owner = User.objects.filter(id = int(validated_data['owner'])).first()
        )
        return project

class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']



class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True,required=False)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
    priority = serializers.CharField(required=True)
    assigned_to =serializers.CharField(required=False)
    project = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(read_only=True,required=False)
    due_date = serializers.DateTimeField(read_only=True,required=False)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'project', 'created_at', 'due_date']

    def validate(self, attrs):
        project = Project.objects.filter(id = int(attrs.get('project'))).first()
        if project is None:
            raise serializers.ValidationError("Please Valid Project Add")
        return attrs

    def create(self, validated_data):
        user = User.objects.filter(id = int(validated_data['assigned_to'])).first()
        if user is None:
            user = None
        project = Project.objects.filter(id = int(validated_data['project'])).first()
        task = Task.objects.create(
            title = validated_data['title'],
            description = validated_data['description'],
            status = validated_data['status'],
            priority = validated_data['priority'],
            assigned_to = user,
            project = project
        )
        return task
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        user = User.objects.filter(id = int(validated_data['assigned_to'])).first()
        if user:
            instance.assigned_to = user
        instance.project = Project.objects.filter(id = int(validated_data.get('project', instance.project.id))).first()
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True,required=False)
    content = serializers.CharField(required=True)
    user =serializers.CharField(required=True)
    task = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(read_only=True,required=False)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']

    def validate_user(self, value):
        user = User.objects.filter(id = int(value)).first()
        if user is None:
            raise serializers.ValidationError("Please Valid user Add")
        return value
    
    def validate_task(self, value):
        task = Task.objects.filter(id = int(value)).first()
        if task is None:
            raise serializers.ValidationError("Please Valid task Add")
        return value

    def create(self, validated_data):
        user = User.objects.filter(id = int(validated_data['user'])).first()
        task = Task.objects.filter(id = int(validated_data['task'])).first()
        comment = Comment.objects.create(
            content = validated_data['content'],
            user = user,
            task = task
        )
        return comment
    
    def update(self,instance, validated_data):
        user = User.objects.filter(id = int(validated_data['user'])).first()
        task = Task.objects.filter(id = int(validated_data['task'])).first()
        
        instance.content = validated_data.get('content',instance.content)
        if user:
            instance.user = user
        if task:
            instance.task = task
        instance.save()
        return instance