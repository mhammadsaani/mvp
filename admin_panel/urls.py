from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/block/', views.block_user, name='block_user'),
    path('users/<int:pk>/unblock/', views.unblock_user, name='unblock_user'),
    path('job-posts/', views.job_post_list, name='job_post_list'),
    path('job-posts/<int:pk>/remove/', views.remove_job_post, name='remove_job_post'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:pk>/remove/', views.remove_teacher, name='remove_teacher'),
    path('teachers/create/', views.create_teacher, name='create_teacher'),
    path('certifications/', views.certification_list, name='certification_list'),
    path('certifications/<int:pk>/verify/', views.verify_certification, name='verify_certification'),
    path('system-config/', views.system_config, name='system_config'),
    path('admin-actions/', views.admin_action_list, name='admin_action_list'),
]