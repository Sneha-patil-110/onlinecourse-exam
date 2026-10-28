# Online Course Exam (Django)

A Django app for online courses with exams.

- Models: Course, Lesson, Enrollment, Question, Choice, Submission
- Admin: course inlines for lessons and questions, question inline for choices
- Views: course details, exam submission, exam result scoring
- Run: `python3 manage.py migrate && python3 seed_data.py && python3 manage.py runserver`
