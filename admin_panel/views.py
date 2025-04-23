from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from accounts.decorators import admin_required
from accounts.models import User
from student.models import JobPost, StudentProfile
from teacher.models import TeacherProfile, Certification
from .models import AdminAction, SystemConfiguration
from .forms import TeacherCreationForm, SystemConfigForm

@login_required
@admin_required
def admin_dashboard(request):
    """
    Admin dashboard view
    """
    # Get counts for dashboard
    student_count = User.objects.filter(user_type='student').count()
    teacher_count = User.objects.filter(user_type='teacher').count()
    job_post_count = JobPost.objects.count()
    certification_count = Certification.objects.count()
    
    # Get recent admin actions
    recent_actions = AdminAction.objects.order_by('-timestamp')[:10]
    
    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'job_post_count': job_post_count,
        'certification_count': certification_count,
        'recent_actions': recent_actions,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@admin_required
def user_list(request):
    """
    List all users
    """
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'users': users,
    }
    
    return render(request, 'admin_panel/user_list.html', context)

@login_required
@admin_required
def block_user(request, pk):
    """
    Block a user
    """
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user.is_blocked = True
        user.save()
        
        # Log admin action
        AdminAction.objects.create(
            admin=request.user,
            action_type='block_user',
            target_user=user,
            description=f'Blocked user: {user.username}'
        )
        
        messages.success(request, f'User {user.username} has been blocked.')
        return redirect('admin_panel:user_list')
    
    return render(request, 'admin_panel/block_user.html', {'user': user})

@login_required
@admin_required
def unblock_user(request, pk):
    """
    Unblock a user
    """
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user.is_blocked = False
        user.save()
        
        # Log admin action
        AdminAction.objects.create(
            admin=request.user,
            action_type='unblock_user',
            target_user=user,
            description=f'Unblocked user: {user.username}'
        )
        
        messages.success(request, f'User {user.username} has been unblocked.')
        return redirect('admin_panel:user_list')
    
    return render(request, 'admin_panel/unblock_user.html', {'user': user})

@login_required
@admin_required
def job_post_list(request):
    """
    List all job posts
    """
    job_posts = JobPost.objects.all().order_by('-created_at')
    
    context = {
        'job_posts': job_posts,
    }
    
    return render(request, 'admin_panel/job_post_list.html', context)

@login_required
@admin_required
def remove_job_post(request, pk):
    """
    Remove a job post
    """
    job_post = get_object_or_404(JobPost, pk=pk)
    
    if request.method == 'POST':
        # Log admin action
        AdminAction.objects.create(
            admin=request.user,
            action_type='remove_job_post',
            target_user=job_post.student.user,
            description=f'Removed job post: {job_post.title}'
        )
        
        job_post.delete()
        messages.success(request, 'Job post has been removed.')
        return redirect('admin_panel:job_post_list')
    
    return render(request, 'admin_panel/remove_job_post.html', {'job_post': job_post})

@login_required
@admin_required
def teacher_list(request):
    """
    List all teachers
    """
    teachers = TeacherProfile.objects.all().order_by('-user__date_joined')
    
    context = {
        'teachers': teachers,
    }
    
    return render(request, 'admin_panel/teacher_list.html', context)

@login_required
@admin_required
def remove_teacher(request, pk):
    """
    Remove a teacher
    """
    teacher = get_object_or_404(TeacherProfile, pk=pk)
    
    if request.method == 'POST':
        # Log admin action
        AdminAction.objects.create(
            admin=request.user,
            action_type='remove_teacher',
            target_user=teacher.user,
            description=f'Removed teacher: {teacher.user.username}'
        )
        
        teacher.user.delete()  # This will cascade delete the teacher profile
        messages.success(request, 'Teacher has been removed.')
        return redirect('admin_panel:teacher_list')
    
    return render(request, 'admin_panel/remove_teacher.html', {'teacher': teacher})

@login_required
@admin_required
def create_teacher(request):
    """
    Create a new teacher account
    """
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'teacher'
            user.save()
            
            # Create teacher profile
            TeacherProfile.objects.create(user=user)
            
            # Log admin action
            AdminAction.objects.create(
                admin=request.user,
                action_type='create_teacher',
                target_user=user,
                description=f'Created teacher account: {user.username}'
            )
            
            messages.success(request, f'Teacher account for {user.username} has been created.')
            return redirect('admin_panel:teacher_list')
    else:
        form = TeacherCreationForm()
    
    return render(request, 'admin_panel/create_teacher.html', {'form': form})

@login_required
@admin_required
def certification_list(request):
    """
    List all certifications
    """
    certifications = Certification.objects.all().order_by('-upload_date')
    
    context = {
        'certifications': certifications,
    }
    
    return render(request, 'admin_panel/certification_list.html', context)

@login_required
@admin_required
def verify_certification(request, pk):
    """
    Verify a certification
    """
    certification = get_object_or_404(Certification, pk=pk)
    
    if request.method == 'POST':
        certification.is_verified = True
        certification.save()
        
        # Log admin action
        AdminAction.objects.create(
            admin=request.user,
            action_type='verify_certification',
            target_user=certification.teacher.user,
            description=f'Verified certification: {certification.title}'
        )
        
        messages.success(request, 'Certification has been verified.')
        return redirect('admin_panel:certification_list')
    
    return render(request, 'admin_panel/verify_certification.html', {'certification': certification})

@login_required
@admin_required
def system_config(request):
    """
    Manage system configuration
    """
    configs = SystemConfiguration.objects.all()
    
    if request.method == 'POST':
        form = SystemConfigForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data.get('key')
            value = form.cleaned_data.get('value')
            description = form.cleaned_data.get('description')
            
            # Update or create configuration
            config, created = SystemConfiguration.objects.update_or_create(
                key=key,
                defaults={
                    'value': value,
                    'description': description,
                    'updated_by': request.user
                }
            )
            
            # Log admin action
            AdminAction.objects.create(
                admin=request.user,
                action_type='update_system_config',
                description=f'Updated system configuration: {key}'
            )
            
            messages.success(request, 'System configuration has been updated.')
            return redirect('admin_panel:system_config')
    else:
        form = SystemConfigForm()
    
    context = {
        'configs': configs,
        'form': form,
    }
    
    return render(request, 'admin_panel/system_config.html', context)

@login_required
@admin_required
def admin_action_list(request):
    """
    List all admin actions
    """
    actions = AdminAction.objects.all().order_by('-timestamp')
    
    context = {
        'actions': actions,
    }
    
    return render(request, 'admin_panel/admin_action_list.html', context)
