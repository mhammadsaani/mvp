from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('job-post/create/', views.create_job_post, name='create_job_post'),
    path('job-post/<int:pk>/', views.job_post_detail, name='job_post_detail'),
    path('job-post/<int:pk>/edit/', views.edit_job_post, name='edit_job_post'),
    path('job-post/<int:pk>/delete/', views.delete_job_post, name='delete_job_post'),
    path('job-post/<int:pk>/requirements-not-met/', views.requirements_not_met, name='requirements_not_met'),
    path('teacher-search/', views.teacher_search, name='teacher_search'),
    path('teacher/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('teacher/<int:pk>/contact/', views.contact_teacher, name='contact_teacher'),
    path('bid/<int:pk>/accept/', views.accept_bid, name='accept_bid'),
    path('bid/<int:pk>/reject/', views.reject_bid, name='reject_bid'),
]