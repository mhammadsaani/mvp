from django.contrib import admin
from .models import TeacherProfile, Certification, TeacherTimetable, CoinTransaction

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'experience_years', 'hourly_rate', 'coins')
    search_fields = ('user__username', 'user__email', 'expertise')
    list_filter = ('experience_years',)

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'issuing_organization', 'issue_date', 'expiry_date', 'is_verified')
    search_fields = ('title', 'teacher__user__username', 'issuing_organization')
    list_filter = ('is_verified', 'issue_date')

@admin.register(TeacherTimetable)
class TeacherTimetableAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'number_of_classes', 'hourly_rate', 'created_at')
    search_fields = ('title', 'teacher__user__username', 'description')
    list_filter = ('created_at',)

@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'amount', 'transaction_type', 'description', 'transaction_date')
    search_fields = ('teacher__user__username', 'description')
    list_filter = ('transaction_type', 'transaction_date')
