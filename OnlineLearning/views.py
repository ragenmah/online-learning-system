from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import Roles, Users, Courses, Enrolls, Fees, FeesPayment
from django.template import RequestContext

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
    courses_count = Courses.objects.all().count()
    courses_of_admins = Courses.objects.filter(user_id=user)     # course created by admins and teachers
    fees_paid = FeesPayment.objects.filter(paid_to=user.id)
    enroll_students = Enrolls.objects.filter(teacher_id=user.id)

    labels = ["Students", "Teachers", "Courses"]
    data = [students_count, teachers_count, courses_count]

    # for city in students_count:
    #     labels.append(city.name)
    # data.append(students_count)
    # data.append(teachers_count)

    context = {
        'users_count': users_count-1,
        'students_count': students_count,
        'enroll_count': enroll_students.count(),
        'teachers_count': teachers_count,
        'courses_count': courses_count,
        'user': user,
        'courses_of_admins': courses_of_admins,
        'fees_paid_count': fees_paid.count(),
        'labels': labels,
        'data': data,
    }
    return context


def ContextForStudents(request):
    userId=request.session['user_id']
    user = Users.objects.get(id=userId)
    teachers_count = Users.objects.filter(user_role_id=request.session['roles_teacher']).values_list('name', flat=True).count()
    all_courses = Courses.objects.all()
    courses_count = Courses.objects.all().count()
    enrolls = Enrolls.objects.filter(user_id=userId)
    fees_paid = FeesPayment.objects.filter(paid_from=user)
    fees = Fees.objects.all()

    fees_data = []
    for elem in all_courses:
        for v in fees:
            if v.course_id.id == elem.id:
                fees_data.append(v)

    context = {
        'user': user,
        'teacher_count': teachers_count,
        'course_count': fees.count(),
        #only courses are shown who has fees
        'fee_paid_count': fees_paid.count(),
        'all_courses': all_courses,
        'enrolls': enrolls,
        'enroll_count': enrolls.count(),
        'fees': fees_data

    }

    return context


def page_not_found_view(request, exception):
    return render(request, '403.html', status=404)

# views.py
def handler404(request, exception):
    context = RequestContext(request)
    err_code = 404
    response = render_to_response('404.html', {"code":err_code}, context)
    response.status_code = 404
    return response