from difflib import SequenceMatcher
from django.db.models import Q

def calculate_similarity_score(teacher_profile, job_post):
    """
    Calculate similarity score between a teacher profile and a job post
    Returns a score between 0 and 100
    """
    # Initialize score components
    subject_match = 0
    experience_match = 0
    education_match = 0
    
    # Subject match (50% weight)
    if job_post.subject.lower() in teacher_profile.expertise.lower():
        subject_match = 50
    else:
        # Partial match using sequence matcher
        subject_similarity = SequenceMatcher(None, 
                                           job_post.subject.lower(), 
                                           teacher_profile.expertise.lower()).ratio()
        subject_match = int(subject_similarity * 50)
    
    # Experience match (30% weight)
    if teacher_profile.experience_years >= job_post.preferred_experience:
        experience_match = 30
    else:
        # Partial match based on percentage of preferred experience
        experience_ratio = teacher_profile.experience_years / max(1, job_post.preferred_experience)
        experience_match = int(min(1, experience_ratio) * 30)
    
    # Education level match (20% weight)
    if hasattr(teacher_profile.user, 'education') and teacher_profile.user.education:
        education_similarity = SequenceMatcher(None, 
                                             job_post.education_level.lower(), 
                                             teacher_profile.user.education.lower()).ratio()
        education_match = int(education_similarity * 20)
    
    # Calculate total score
    total_score = subject_match + experience_match + education_match
    
    return total_score

def get_eligible_teachers_for_job(job_post, min_similarity=60):
    """
    Get all teachers eligible to bid on a job post based on similarity score
    """
    from teacher.models import TeacherProfile
    
    eligible_teachers = []
    all_teachers = TeacherProfile.objects.filter(user__is_active=True, user__is_blocked=False)
    
    for teacher in all_teachers:
        similarity_score = calculate_similarity_score(teacher, job_post)
        teacher.similarity_score = similarity_score
        
        if similarity_score >= min_similarity:
            eligible_teachers.append(teacher)
    
    # Sort by similarity score (descending)
    eligible_teachers.sort(key=lambda x: x.similarity_score, reverse=True)
    
    return eligible_teachers