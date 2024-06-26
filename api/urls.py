from django.urls import path
from .views import UserRegisterView, UserLoginView, UserDetailView, ProjectListView, ProjectDetailView, TaskListView, TaskDetailView, CommentListView, CommentDetailView

urlpatterns = [
    path('users/register/', UserRegisterView.as_view(), name='register'),
    path('users/login/', UserLoginView.as_view(), name='login'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),

    path('projects/<int:project_id>/tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    
    path('tasks/<int:task_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
