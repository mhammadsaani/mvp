from django.contrib import admin
from .models import StudentProfile, JobPost, TeacherBid, StudentTeacherContact

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'education_level', 'subjects_of_interest')
    search_fields = ('user__username', 'user__email', 'subjects_of_interest')
    list_filter = ('education_level',)

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'subject', 'status', 'current_bid_cycle', 'created_at')
    search_fields = ('title', 'student__user__username', 'description', 'subject')
    list_filter = ('status', 'current_bid_cycle', 'created_at')
    readonly_fields = ('current_bid_cycle', 'max_bids_current_cycle')

@admin.register(TeacherBid)
class TeacherBidAdmin(admin.ModelAdmin):
    list_display = ('job_post', 'teacher', 'hourly_rate', 'similarity_score', 'status', 'created_at')
    search_fields = ('job_post__title', 'teacher__user__username', 'proposal')
    list_filter = ('status', 'created_at')
    readonly_fields = ('similarity_score',)

@admin.register(StudentTeacherContact)
class StudentTeacherContactAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'job_post', 'coins_used', 'created_at')
    search_fields = ('student__user__username', 'teacher__user__username', 'message')
    list_filter = ('created_at',)
