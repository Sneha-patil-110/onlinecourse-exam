"""Load sample course data and local test accounts (development only)."""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlinecourse_site.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from onlinecourse.models import Choice, Course, Lesson, Question  # noqa: E402

course, _ = Course.objects.get_or_create(
    name="Python Basics", defaults={"description": "Intro to Python for beginners."}
)
Lesson.objects.get_or_create(course=course, title="Variables and types")
Lesson.objects.get_or_create(course=course, title="Functions")

q1, _ = Question.objects.get_or_create(course=course, text="Which keyword defines a function?", defaults={"grade": 1})
for text, correct in [("def", True), ("func", False), ("lambda_fn", False)]:
    Choice.objects.get_or_create(question=q1, text=text, defaults={"is_correct": correct})

q2, _ = Question.objects.get_or_create(course=course, text="Which are immutable types? (select all)", defaults={"grade": 1})
for text, correct in [("tuple", True), ("list", False), ("str", True)]:
    Choice.objects.get_or_create(question=q2, text=text, defaults={"is_correct": correct})

admin_user, created = User.objects.get_or_create(username="admin", defaults={"is_staff": True, "is_superuser": True})
if created:
    admin_user.set_password("AdminTest!2026")
    admin_user.save()
student, created = User.objects.get_or_create(username="student")
if created:
    student.set_password("StudentTest!2026")
    student.save()
print("seeded")
