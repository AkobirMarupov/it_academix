from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from account.models import User, Profile, Story


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "email", "phone_number", "is_active", "is_staff")
    list_display_links = ("id", "email", "phone_number")
    search_fields = ("email", "phone_number")
    list_filter = ("is_active", "is_staff")
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('phone_number',)}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'groups', 'user_permissions'),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }), 
    )
    
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "phone_number", "birth_date", "avatar_preview")
    list_display_links = ("id", "user", "full_name")
    search_fields = ("full_name", "phone_number", "user__email")

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;" />', obj.avatar.url)
        return "—"
    avatar_preview.short_description = "Avatar"




@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "expires_at", 'video', 'image', 'is_active')
    list_display_links = ("id", "user", "title")
    search_fields = ("user__email", "title")
    list_filter = ("expires_at",)
    