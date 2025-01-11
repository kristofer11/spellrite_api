# api/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher, SpellingList, SpellingListWord

@admin.register(Teacher)
class TeacherAdmin(UserAdmin):
    """
    Admin interface for the custom Teacher model.
    Extends Django's UserAdmin to include additional fields.
    """
    model = Teacher
    list_display = (
        'username', 'first_name', 'last_name', 'email',
        'organization', 'class_name', 'access_code', 'is_staff', 'is_active'
    )
    list_filter = ('is_staff', 'is_active', 'organization', 'class_name')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('organization', 'class_name', 'access_code')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('organization', 'class_name', 'access_code')}),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'organization', 'class_name', 'access_code')
    ordering = ('username',)

@admin.register(SpellingList)
class SpellingListAdmin(admin.ModelAdmin):
    """
    Admin interface for the SpellingList model.
    """
    list_display = ('list_id', 'list_name', 'teacher', 'created_at', 'updated_at')
    search_fields = ('list_name', 'teacher__first_name', 'teacher__last_name')
    list_filter = ('teacher', 'created_at')

@admin.register(SpellingListWord)
class SpellingListWordAdmin(admin.ModelAdmin):
    """
    Admin interface for the SpellingListWord model.
    """
    list_display = ('list_word_id', 'spelling_list', 'word', 'created_at', 'updated_at')
    search_fields = ('word', 'spelling_list__list_name')
    list_filter = ('spelling_list', 'created_at')