from django.contrib import admin
from .models import AdminAction, SystemConfiguration

@admin.register(AdminAction)
class AdminActionAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'admin', 'target_user', 'timestamp')
    search_fields = ('admin__username', 'target_user__username', 'description')
    list_filter = ('action_type', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'last_updated', 'updated_by')
    search_fields = ('key', 'value', 'description')
    list_filter = ('last_updated',)
    readonly_fields = ('last_updated',)
