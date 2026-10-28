"""Course detail, exam submission and exam result views."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Choice, Course, Enrollment, Submission


def course_details(request, course_id):
    """Show the course name, its lessons and the exam questions with choices."""
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


@login_required
def submit(request, course_id):
    """Store the selected choices for the logged-in user as a new submission."""
    course = get_object_or_404(Course, pk=course_id)
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    selected_ids = request.POST.getlist("choice")
    submission.choices.set(Choice.objects.filter(pk__in=selected_ids))
    return redirect("onlinecourse:show_exam_result", course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    """Score a submission: each question's grade counts only when all its answers are right."""
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id, enrollment__course=course)
    selected = list(submission.choices.all())

    total = 0
    earned = 0
    rows = []
    for question in course.questions.all():
        chosen = [c for c in selected if c.question_id == question.id]
        correct = question.is_correct(chosen)
        total += question.grade
        if correct:
            earned += question.grade
        rows.append({"question": question, "chosen": chosen, "correct": correct})

    percent = round(100 * earned / total) if total else 0
    context = {
        "course": course,
        "submission": submission,
        "rows": rows,
        "earned": earned,
        "total": total,
        "percent": percent,
        "passed": percent >= 60,
    }
    return render(request, "onlinecourse/exam_result_bootstrap.html", context)
