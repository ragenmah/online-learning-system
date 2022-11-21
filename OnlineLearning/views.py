from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import Roles, Users, Courses, Enrolls
from django.contrib.auth.hashers import make_password

class HomeView(TemplateView):

    template_name = "onlineLearning/home.html"

@login_required
def DashboardView(request):
    # return redirect('teachers:dashboard')
    if request.user.is_student:
        return redirect('students:dashboard')
    if request.user.is_teacher:
        return redirect('teachers:dashboard')
    if request.user.is_superuser:
        return redirect('admins:dashboard')

# for sharing data to all html pages
def AllContextItems(request):
    user = Users.objects.get(id=request.session['user_id'])
    users_count = Users.objects.all().count()
    students_count = Users.objects.filter(user_role_id=request.session['roles_std']).values_list('name', flat=True).count()
    teachers_count = Users.objects.filter(user_role_id=request.session['roles_teacher']).values_list('name', flat=True).count()
    courses_count = Courses.objects.filter(user_id=user).count()
    courses_of_admins = Courses.objects.filter(user_id=user)     # course created by admins and teachers


    context = {
        'users_count': users_count,
        'students_count': students_count,
        'teachers_count': teachers_count,
        'courses_count': courses_count,
        'user': user,
        'courses_of_admins': courses_of_admins,
    }
    return context

def ContextForStudents(request):
    userId=request.session['user_id']
    user = Users.objects.get(id=userId)
    teachers_count = Users.objects.filter(user_role_id=request.session['roles_teacher']).values_list('name', flat=True).count()
    all_courses = Courses.objects.all()
    courses_count = Courses.objects.all().count()
    enrolls = Enrolls.objects.filter(user_id=userId)

    context = {
        'user': user,
        'teacher_count': teachers_count,
        'course_count': courses_count,
        'all_courses': all_courses,
        'enrolls': enrolls,
        'enroll_count': enrolls.count(),
    }

    return context
