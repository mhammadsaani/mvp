from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from accounts.decorators import student_required
from .models import StudentProfile, JobPost, TeacherBid, StudentTeacherContact
from teacher.models import TeacherProfile
from .forms import JobPostForm, StudentTeacherContactForm
from teacher.utils import get_eligible_teachers_for_job

@login_required
@student_required
def student_dashboard(request):
    """
    Student dashboard view
    """
    # Get student's job posts
    job_posts = JobPost.objects.filter(student__user=request.user).order_by('-created_at')
    
    # Get bids on student's job posts
    bids = TeacherBid.objects.filter(job_post__student__user=request.user).order_by('-created_at')
    
    context = {
        'job_posts': job_posts,
        'bids': bids,
    }
    
    return render(request, 'student/dashboard.html', context)

@login_required
@student_required
def create_job_post(request):
    """
    Create a new job post
    """
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.student = request.user.student_profile
            job_post.save()
            messages.success(request, 'Job post created successfully!')
            return redirect('student:job_post_detail', pk=job_post.pk)
    else:
        form = JobPostForm()
    
    return render(request, 'student/create_job_post.html', {'form': form})

@login_required
@student_required
def job_post_detail(request, pk):
    """
    View job post details
    """
    job_post = get_object_or_404(JobPost, pk=pk)
    
    # Check if the job post belongs to the current user
    if job_post.student.user != request.user:
        return HttpResponseForbidden("You don't have permission to view this job post.")
    
    # Get bids for this job post
    bids = TeacherBid.objects.filter(job_post=job_post).order_by('-similarity_score')
    
    context = {
        'job_post': job_post,
        'bids': bids,
    }
    
    return render(request, 'student/job_post_detail.html', context)

@login_required
@student_required
def edit_job_post(request, pk):
    """
    Edit a job post
    """
    job_post = get_object_or_404(JobPost, pk=pk)
    
    # Check if the job post belongs to the current user
    if job_post.student.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this job post.")
    
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job post updated successfully!')
            return redirect('student:job_post_detail', pk=job_post.pk)
    else:
        form = JobPostForm(instance=job_post)
    
    return render(request, 'student/edit_job_post.html', {'form': form, 'job_post': job_post})

@login_required
@student_required
def delete_job_post(request, pk):
    """
    Delete a job post
    """
    job_post = get_object_or_404(JobPost, pk=pk)
    
    # Check if the job post belongs to the current user
    if job_post.student.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this job post.")
    
    if request.method == 'POST':
        job_post.delete()
        messages.success(request, 'Job post deleted successfully!')
        return redirect('student:dashboard')
    
    return render(request, 'student/delete_job_post.html', {'job_post': job_post})

@login_required
@student_required
def requirements_not_met(request, pk):
    """
    Mark job post requirements as not met to allow more teachers to bid
    """
    job_post = get_object_or_404(JobPost, pk=pk)
    
    # Check if the job post belongs to the current user
    if job_post.student.user != request.user:
        return HttpResponseForbidden("You don't have permission to update this job post.")
    
    # Increment the bid cycle and update max bids
    job_post.current_bid_cycle += 1
    job_post.max_bids_current_cycle = 5  # 5 more teachers per cycle
    job_post.save()
    
    messages.success(request, 'More teachers can now bid on your job post.')
    return redirect('student:job_post_detail', pk=job_post.pk)

@login_required
@student_required
def teacher_search(request):
    """
    Search for teachers
    """
    query = request.GET.get('q', '')
    teachers = TeacherProfile.objects.filter(user__is_active=True, user__is_blocked=False)
    
    if query:
        teachers = teachers.filter(
            expertise__icontains=query
        ) | teachers.filter(
            user__first_name__icontains=query
        ) | teachers.filter(
            user__last_name__icontains=query
        )
    
    context = {
        'teachers': teachers,
        'query': query,
    }
    
    return render(request, 'student/teacher_search.html', context)

@login_required
@student_required
def teacher_detail(request, pk):
    """
    View teacher profile details
    """
    teacher = get_object_or_404(TeacherProfile, pk=pk)
    
    # Check if teacher is active and not blocked
    if not teacher.user.is_active or teacher.user.is_blocked:
        messages.error(request, 'This teacher profile is not available.')
        return redirect('student:teacher_search')
    
    context = {
        'teacher': teacher,
    }
    
    return render(request, 'student/teacher_detail.html', context)

@login_required
@student_required
def contact_teacher(request, pk):
    """
    Contact a teacher directly
    """
    teacher = get_object_or_404(TeacherProfile, pk=pk)
    
    # Check if teacher is active and not blocked
    if not teacher.user.is_active or teacher.user.is_blocked:
        messages.error(request, 'This teacher profile is not available.')
        return redirect('student:teacher_search')
    
    if request.method == 'POST':
        form = StudentTeacherContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.student = request.user.student_profile
            contact.teacher = teacher
            contact.save()
            messages.success(request, f'Your message has been sent to {teacher.user.get_full_name()}.')
            return redirect('student:teacher_detail', pk=teacher.pk)
    else:
        form = StudentTeacherContactForm()
    
    context = {
        'teacher': teacher,
        'form': form,
    }
    
    return render(request, 'student/contact_teacher.html', context)

@login_required
@student_required
def accept_bid(request, pk):
    """
    Accept a teacher's bid
    """
    bid = get_object_or_404(TeacherBid, pk=pk)
    
    # Check if the bid is on a job post that belongs to the current user
    if bid.job_post.student.user != request.user:
        return HttpResponseForbidden("You don't have permission to accept this bid.")
    
    # Update bid status
    bid.status = 'accepted'
    bid.save()
    
    # Update job post status
    bid.job_post.status = 'assigned'
    bid.job_post.save()
    
    # Reject all other bids
    TeacherBid.objects.filter(job_post=bid.job_post).exclude(pk=bid.pk).update(status='rejected')
    
    messages.success(request, f'You have accepted the bid from {bid.teacher.user.get_full_name()}.')
    return redirect('student:job_post_detail', pk=bid.job_post.pk)

@login_required
@student_required
def reject_bid(request, pk):
    """
    Reject a teacher's bid
    """
    bid = get_object_or_404(TeacherBid, pk=pk)
    
    # Check if the bid is on a job post that belongs to the current user
    if bid.job_post.student.user != request.user:
        return HttpResponseForbidden("You don't have permission to reject this bid.")
    
    # Update bid status
    bid.status = 'rejected'
    bid.save()
    
    messages.success(request, f'You have rejected the bid from {bid.teacher.user.get_full_name()}.')
    return redirect('student:job_post_detail', pk=bid.job_post.pk)
