from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from student.models import StudentProfile
from teacher.models import TeacherProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a profile for a user when they are created
    """
    if created:
        if instance.user_type == 'student':
            StudentProfile.objects.create(user=instance)
        elif instance.user_type == 'teacher':
            TeacherProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the profile when the user is saved
    """
    if instance.user_type == 'student':
        if hasattr(instance, 'student_profile'):
            instance.student_profile.save()
        else:
            StudentProfile.objects.create(user=instance)
    elif instance.user_type == 'teacher':
        if hasattr(instance, 'teacher_profile'):
            instance.teacher_profile.save()
        else:
            TeacherProfile.objects.create(user=instance)