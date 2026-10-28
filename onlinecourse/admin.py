"""Admin site registration with inline questions and choices."""
from django.contrib import admin

from .models import Choice, Course, Enrollment, Lesson, Question, Submission

# Shown when the admin site is used: the Lesson, Question and Choice inlines.

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("text", "course", "grade")

class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course")

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ("name",)

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Enrollment)
admin.site.register(Submission)
