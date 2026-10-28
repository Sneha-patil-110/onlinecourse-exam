"""Course, lesson, exam question, choice, enrollment and submission models."""
from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} in {self.course}"


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=300)
    grade = models.IntegerField(default=1, help_text="Points for a correct answer")

    def __str__(self):
        return self.text

    def is_correct(self, selected_choices):
        """True when the selected choices are exactly the correct ones."""
        correct = set(self.choice_set.filter(is_correct=True).values_list("id", flat=True))
        return correct == {c.id for c in selected_choices}


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="submissions")
    choices = models.ManyToManyField(Choice)
    date_submitted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Submission {self.id} by {self.enrollment.user}"
