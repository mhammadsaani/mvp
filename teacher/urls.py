from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='dashboard'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('certification/add/', views.add_certification, name='add_certification'),
    path('certification/<int:pk>/edit/', views.edit_certification, name='edit_certification'),
    path('certification/<int:pk>/delete/', views.delete_certification, name='delete_certification'),
    path('timetable/create/', views.create_timetable, name='create_timetable'),
    path('timetable/<int:pk>/edit/', views.edit_timetable, name='edit_timetable'),
    path('timetable/<int:pk>/delete/', views.delete_timetable, name='delete_timetable'),
    path('job-posts/', views.available_job_posts, name='available_job_posts'),
    path('job-post/<int:pk>/', views.job_post_detail, name='job_post_detail'),
    path('job-post/<int:pk>/bid/', views.create_bid, name='create_bid'),
    path('bid/<int:pk>/edit/', views.edit_bid, name='edit_bid'),
    path('bid/<int:pk>/delete/', views.delete_bid, name='delete_bid'),
    path('coins/buy/', views.buy_coins, name='buy_coins'),
    path('coins/transactions/', views.coin_transactions, name='coin_transactions'),
    path('student/<int:pk>/contact/', views.contact_student, name='contact_student'),
]