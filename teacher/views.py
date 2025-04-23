from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from accounts.decorators import teacher_required
from .models import TeacherProfile, Certification, TeacherTimetable, CoinTransaction
from student.models import JobPost, TeacherBid, StudentTeacherContact
from .forms import TeacherProfileForm, CertificationForm, TeacherTimetableForm, BidForm, CoinPurchaseForm
from .utils import calculate_similarity_score, get_eligible_teachers_for_job

@login_required
@teacher_required
def teacher_dashboard(request):
    """
    Teacher dashboard view
    """
    # Get teacher's bids
    bids = TeacherBid.objects.filter(teacher__user=request.user).order_by('-created_at')
    
    # Get teacher's certifications
    certifications = Certification.objects.filter(teacher__user=request.user).order_by('-upload_date')
    
    # Get teacher's timetables
    timetables = TeacherTimetable.objects.filter(teacher__user=request.user).order_by('-created_at')
    
    # Get teacher's coin transactions
    transactions = CoinTransaction.objects.filter(teacher__user=request.user).order_by('-timestamp')
    
    context = {
        'bids': bids,
        'certifications': certifications,
        'timetables': timetables,
        'transactions': transactions,
    }
    
    return render(request, 'teacher/dashboard.html', context)

@login_required
@teacher_required
def create_profile(request):
    """
    Create teacher profile
    """
    # Check if teacher already has a profile
    if hasattr(request.user, 'teacher_profile'):
        messages.info(request, 'You already have a teacher profile.')
        return redirect('teacher:edit_profile')
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Teacher profile created successfully!')
            return redirect('teacher:dashboard')
    else:
        form = TeacherProfileForm()
    
    return render(request, 'teacher/create_profile.html', {'form': form})

@login_required
@teacher_required
def edit_profile(request):
    """
    Edit teacher profile
    """
    # Get teacher profile or create if it doesn't exist
    profile, created = TeacherProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher profile updated successfully!')
            return redirect('teacher:dashboard')
    else:
        form = TeacherProfileForm(instance=profile)
    
    return render(request, 'teacher/edit_profile.html', {'form': form})

@login_required
@teacher_required
def add_certification(request):
    """
    Add a certification
    """
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.teacher = request.user.teacher_profile
            certification.save()
            messages.success(request, 'Certification added successfully!')
            return redirect('teacher:dashboard')
    else:
        form = CertificationForm()
    
    return render(request, 'teacher/add_certification.html', {'form': form})

@login_required
@teacher_required
def edit_certification(request, pk):
    """
    Edit a certification
    """
    certification = get_object_or_404(Certification, pk=pk)
    
    # Check if the certification belongs to the current user
    if certification.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this certification.")
    
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certification updated successfully!')
            return redirect('teacher:dashboard')
    else:
        form = CertificationForm(instance=certification)
    
    return render(request, 'teacher/edit_certification.html', {'form': form, 'certification': certification})

@login_required
@teacher_required
def delete_certification(request, pk):
    """
    Delete a certification
    """
    certification = get_object_or_404(Certification, pk=pk)
    
    # Check if the certification belongs to the current user
    if certification.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this certification.")
    
    if request.method == 'POST':
        certification.delete()
        messages.success(request, 'Certification deleted successfully!')
        return redirect('teacher:dashboard')
    
    return render(request, 'teacher/delete_certification.html', {'certification': certification})

@login_required
@teacher_required
def create_timetable(request):
    """
    Create a timetable
    """
    if request.method == 'POST':
        form = TeacherTimetableForm(request.POST)
        if form.is_valid():
            timetable = form.save(commit=False)
            timetable.teacher = request.user.teacher_profile
            timetable.save()
            messages.success(request, 'Timetable created successfully!')
            return redirect('teacher:dashboard')
    else:
        form = TeacherTimetableForm()
    
    return render(request, 'teacher/create_timetable.html', {'form': form})

@login_required
@teacher_required
def edit_timetable(request, pk):
    """
    Edit a timetable
    """
    timetable = get_object_or_404(TeacherTimetable, pk=pk)
    
    # Check if the timetable belongs to the current user
    if timetable.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this timetable.")
    
    if request.method == 'POST':
        form = TeacherTimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable updated successfully!')
            return redirect('teacher:dashboard')
    else:
        form = TeacherTimetableForm(instance=timetable)
    
    return render(request, 'teacher/edit_timetable.html', {'form': form, 'timetable': timetable})

@login_required
@teacher_required
def delete_timetable(request, pk):
    """
    Delete a timetable
    """
    timetable = get_object_or_404(TeacherTimetable, pk=pk)
    
    # Check if the timetable belongs to the current user
    if timetable.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this timetable.")
    
    if request.method == 'POST':
        timetable.delete()
        messages.success(request, 'Timetable deleted successfully!')
        return redirect('teacher:dashboard')
    
    return render(request, 'teacher/delete_timetable.html', {'timetable': timetable})

@login_required
@teacher_required
def available_job_posts(request):
    """
    View available job posts
    """
    # Get all active job posts
    job_posts = JobPost.objects.filter(status='open').order_by('-created_at')
    
    # Calculate similarity score for each job post
    for job_post in job_posts:
        job_post.similarity_score = calculate_similarity_score(request.user.teacher_profile, job_post)
        
        # Check if teacher has already bid on this job post
        job_post.has_bid = TeacherBid.objects.filter(job_post=job_post, teacher=request.user.teacher_profile).exists()
        
        # Check if teacher is eligible to bid (similarity score >= 60%)
        job_post.is_eligible = job_post.similarity_score >= 60
        
        # Check if job post has reached maximum bids for current cycle
        current_bids_count = TeacherBid.objects.filter(job_post=job_post).count()
        job_post.max_bids_reached = current_bids_count >= job_post.max_bids_current_cycle
    
    context = {
        'job_posts': job_posts,
    }
    
    return render(request, 'teacher/available_job_posts.html', context)

@login_required
@teacher_required
def job_post_detail(request, pk):
    """
    View job post details
    """
    job_post = get_object_or_404(JobPost, pk=pk)
    
    # Calculate similarity score
    similarity_score = calculate_similarity_score(request.user.teacher_profile, job_post)
    
    # Check if teacher has already bid on this job post
    has_bid = TeacherBid.objects.filter(job_post=job_post, teacher=request.user.teacher_profile).exists()
    
    # Check if teacher is eligible to bid (similarity score >= 60%)
    is_eligible = similarity_score >= 60
    
    # Check if job post has reached maximum bids for current cycle
    current_bids_count = TeacherBid.objects.filter(job_post=job_post).count()
    max_bids_reached = current_bids_count >= job_post.max_bids_current_cycle
    
    context = {
        'job_post': job_post,
        'similarity_score': similarity_score,
        'has_bid': has_bid,
        'is_eligible': is_eligible,
        'max_bids_reached': max_bids_reached,
    }
    
    return render(request, 'teacher/job_post_detail.html', context)

@login_required
@teacher_required
def create_bid(request, pk):
    """
    Create a bid on a job post
    """
    job_post = get_object_or_404(JobPost, pk=pk)
    
    # Calculate similarity score
    similarity_score = calculate_similarity_score(request.user.teacher_profile, job_post)
    
    # Check if teacher is eligible to bid (similarity score >= 60%)
    if similarity_score < 60:
        messages.error(request, 'You are not eligible to bid on this job post. Your similarity score is below 60%.')
        return redirect('teacher:job_post_detail', pk=job_post.pk)
    
    # Check if teacher has already bid on this job post
    if TeacherBid.objects.filter(job_post=job_post, teacher=request.user.teacher_profile).exists():
        messages.error(request, 'You have already bid on this job post.')
        return redirect('teacher:job_post_detail', pk=job_post.pk)
    
    # Check if job post has reached maximum bids for current cycle
    current_bids_count = TeacherBid.objects.filter(job_post=job_post).count()
    if current_bids_count >= job_post.max_bids_current_cycle:
        messages.error(request, 'This job post has reached the maximum number of bids for the current cycle.')
        return redirect('teacher:job_post_detail', pk=job_post.pk)
    
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.job_post = job_post
            bid.teacher = request.user.teacher_profile
            bid.similarity_score = similarity_score
            bid.save()
            messages.success(request, 'Bid created successfully!')
            return redirect('teacher:job_post_detail', pk=job_post.pk)
    else:
        form = BidForm()
    
    context = {
        'form': form,
        'job_post': job_post,
        'similarity_score': similarity_score,
    }
    
    return render(request, 'teacher/create_bid.html', context)

@login_required
@teacher_required
def edit_bid(request, pk):
    """
    Edit a bid
    """
    bid = get_object_or_404(TeacherBid, pk=pk)
    
    # Check if the bid belongs to the current user
    if bid.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this bid.")
    
    # Check if the bid can be edited (only if status is 'pending')
    if bid.status != 'pending':
        messages.error(request, 'You cannot edit this bid as it has already been processed.')
        return redirect('teacher:dashboard')
    
    if request.method == 'POST':
        form = BidForm(request.POST, instance=bid)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bid updated successfully!')
            return redirect('teacher:dashboard')
    else:
        form = BidForm(instance=bid)
    
    context = {
        'form': form,
        'bid': bid,
    }
    
    return render(request, 'teacher/edit_bid.html', context)

@login_required
@teacher_required
def delete_bid(request, pk):
    """
    Delete a bid
    """
    bid = get_object_or_404(TeacherBid, pk=pk)
    
    # Check if the bid belongs to the current user
    if bid.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this bid.")
    
    # Check if the bid can be deleted (only if status is 'pending')
    if bid.status != 'pending':
        messages.error(request, 'You cannot delete this bid as it has already been processed.')
        return redirect('teacher:dashboard')
    
    if request.method == 'POST':
        bid.delete()
        messages.success(request, 'Bid deleted successfully!')
        return redirect('teacher:dashboard')
    
    return render(request, 'teacher/delete_bid.html', {'bid': bid})

@login_required
@teacher_required
def buy_coins(request):
    """
    Buy coins
    """
    if request.method == 'POST':
        form = CoinPurchaseForm(request.POST)
        if form.is_valid():
            coins_amount = form.cleaned_data.get('coins_amount')
            payment_method = form.cleaned_data.get('payment_method')
            
            # Create a coin transaction
            transaction = CoinTransaction.objects.create(
                teacher=request.user.teacher_profile,
                transaction_type='purchase',
                amount=coins_amount,
                description=f'Purchased {coins_amount} coins via {payment_method}'
            )
            
            # Update teacher's coin balance
            request.user.teacher_profile.coins += coins_amount
            request.user.teacher_profile.save()
            
            messages.success(request, f'You have successfully purchased {coins_amount} coins!')
            return redirect('teacher:dashboard')
    else:
        form = CoinPurchaseForm()
    
    return render(request, 'teacher/buy_coins.html', {'form': form})

@login_required
@teacher_required
def coin_transactions(request):
    """
    View coin transactions
    """
    transactions = CoinTransaction.objects.filter(teacher=request.user.teacher_profile).order_by('-timestamp')
    
    return render(request, 'teacher/coin_transactions.html', {'transactions': transactions})

@login_required
@teacher_required
def contact_student(request, pk):
    """
    Contact a student directly
    """
    job_post = get_object_or_404(JobPost, pk=pk)
    
    # Check if job post is active
    if job_post.status != 'open':
        messages.error(request, 'This job post is no longer active.')
        return redirect('teacher:available_job_posts')
    
    # Check if teacher is eligible to contact student
    is_free_contact = False
    
    # Free contact if job post is less than 5 minutes old and teacher is in top 5 similarity
    time_diff = timezone.now() - job_post.created_at
    if time_diff.total_seconds() < 300:  # 5 minutes in seconds
        # Get top 5 teachers by similarity score
        eligible_teachers = get_eligible_teachers_for_job(job_post)[:5]
        is_free_contact = request.user.teacher_profile in eligible_teachers
    
    # Check if teacher has enough coins
    if not is_free_contact and request.user.teacher_profile.coins < 1:
        messages.error(request, 'You do not have enough coins to contact this student. Please buy more coins.')
        return redirect('teacher:buy_coins')
    
    if request.method == 'POST':
        # Create contact record
        contact = StudentTeacherContact.objects.create(
            student=job_post.student,
            teacher=request.user.teacher_profile,
            job_post=job_post,
            message=request.POST.get('message', ''),
            coins_used=0 if is_free_contact else 1
        )
        
        # Deduct coins if not free
        if not is_free_contact:
            request.user.teacher_profile.coins -= 1
            request.user.teacher_profile.save()
            
            # Create transaction record
            CoinTransaction.objects.create(
                teacher=request.user.teacher_profile,
                transaction_type='usage',
                amount=1,
                description=f'Contact student for job post: {job_post.title}'
            )
        
        messages.success(request, f'Your message has been sent to {job_post.student.user.get_full_name()}.')
        return redirect('teacher:job_post_detail', pk=job_post.pk)
    
    context = {
        'job_post': job_post,
        'is_free_contact': is_free_contact,
    }
    
    return render(request, 'teacher/contact_student.html', context)
