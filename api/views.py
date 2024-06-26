from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Project, Task, Comment
from .serializers import *
from django.http import Http404

class UserRegisterView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data,many=False)
        response = dict()
        if serializer.is_valid():
            serializer.save()
            response['status'] = status.HTTP_201_CREATED
            response['message'] = "Create New User Account"
        else:
            response['error'] = serializer.errors
            response['status'] = status.HTTP_400_BAD_REQUEST
            response['message'] = "Bad Request"
        return Response(response,status=response['status'])

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):

    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self,request,pk,format = None,):
       
        user = self.get_object(pk)
        response = dict()
        if user:
            serializer  = UserSerializer(instance = user)
            response['data'] = serializer.data
            response['status'] = status.HTTP_200_OK
            response['message'] = "Get User Detail"
        else:
            response['status'] = status.HTTP_400_BAD_REQUEST
            response['message'] = "BAD REQUEST"
        return Response(response,status=response['status'])
    
    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







class ProjectListView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        snippets = Project.objects.all()
        serializer = ProjectCrearteSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectCrearteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, project_id):
        try:
            return Project.objects.filter(pk=project_id).first()
        except Project.DoesNotExist:
            raise Http404
    def get(self, request,project_id, format=None):

        project = project = self.get_object(project_id)
        task = Task.objects.filter(project = project)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)

    def post(self, request,project_id, format=None):
        project = self.get_object(project_id)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, task_id):
        try:
            return Task.objects.filter(pk=task_id).first()
        except Task.DoesNotExist:
            raise Http404
    def get(self, request,task_id, format=None):

        task= self.get_object(task_id)
        comment = Comment.objects.filter(task = task)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request,task_id, format=None):
        task = self.get_object(task_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)