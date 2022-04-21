from django.contrib import admin
from .models import Course
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'slug', 'description', 'images', 'category')
    prepopulated_fields = {'slug': ('course_name',)}
admin.site.register(Course, CourseAdmin)
