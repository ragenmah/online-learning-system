import os

from django.shortcuts import render,redirect
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView
from .forms import RolesForm, CourseForm
from teachers.forms import CourseResourceForm, CourseQuestionForm, FeesForm
from accounts.forms import UserEditForm, ChangePasswordForm
from accounts.models import Roles, Users, Enrolls, FeesPayment, Courses, Duration, Fees, Tests, Resources
from django.contrib import messages
from OnlineLearning import views
from accounts.decorators import unauthenticated_user
import traceback
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

roles_std = Roles.objects.get(role_title='student').id
roles_teacher = Roles.objects.get(role_title='teacher').id


def DashboardView(request):
    return render(request, "admins/dashboard.html", views.AllContextItems(request))


# Roles
def RolesView(request):
    users = Users.objects.get(id=request.session['user_id'])
    roles = Roles.objects.all()
    return render(request, "admins/roles.html", {'roles': roles, 'user': users})


def RolesCreateView(request):
    users = Users.objects.get(id=request.session['user_id'])
    if request.method=="POST":
        form = RolesForm(request.POST)
        if form.is_valid:
            try:
                new = Roles.objects.filter(role_title=form['role_title'].value())
                if new.exists():
                    messages.error(request, 'Selected role already added.')
                    return render(request, 'admins/add_roles.html', {'form': RolesForm(request.GET)})

                else:form.save()
                messages.success(request, 'Role added successfully.')
            except:
                pass
    form = RolesForm()
    return render(request, "admins/add_roles.html", {'form': form, 'user': users})


def RolesDeleteView(request,id):
    role = Roles.objects.get(id=id)
    role.delete()
    roles = Roles.objects.all()

    messages.success(request, 'Selected role is deleted .')
    return render(request, 'admins/roles.html', {'roles': roles})


def RolesEditView(request, id):
    users = Users.objects.get(id=request.session['user_id'])
    roles = Roles.objects.get(id=id)

    form = RolesForm(instance=roles)

    return render(request, 'admins/edit_roles.html', {'roles': roles, 'user': users, 'form': form,})


def RolesUpdateView(request, id):
    if request.method == "POST":
        roles = Roles.objects.get(id=id)
        form = RolesForm(request.POST, instance=roles)

        if form.is_valid:
            form.save()
            messages.success(request, 'Selected role is edited .')
            return redirect("admins:roles")
    return render(request, 'admins/edit_roles.html', {'roles': roles})
# end roles


# Courses
def CourseView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.filter(user_id=users)
    return render(request, 'admins/courses.html', {'courses': courses, 'user': users})


def CourseViewAll(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.all()
    return render(request, 'admins/view_all_courses.html', {'courses': courses, 'user': users})


def CourseCreateView(request):
    if request.method == "POST":
        users = Users.objects.get(id=request.session['user_id'])
        form = CourseForm(request.POST, request.FILES, instance=users)

        course = Courses(
            code=request.POST.get('code'),
            course_title=request.POST.get('course_title'),
            course_description=request.POST.get('course_description'),
            user_id=users,
            course_thumbnail=request.FILES['course_thumbnail']
        )

        if form.is_valid:
            try:
                new = Courses.objects.filter(course_title=request.POST.get('course_title'), user_id=users)
                if new.exists():
                    messages.error(request, 'The courses already added.')
                else:
                    course.save()
                    messages.success(request, 'Course has been added successfully.')
                    return redirect('admins:courses')
            except:
                pass
    form = CourseForm()
    return render(request, "admins/add_courses.html", {'form': form})


@unauthenticated_user
def CourseUpdateView(request, id):
    course = Courses.objects.get(id=id)
    form = CourseForm(instance=course)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, 'Course has been updated successfully.')
                return redirect('admins:courses')
            except:
                pass
    return render(request, "admins/edit_courses.html", {'form': form})


@unauthenticated_user
def CourseDeleteView(request, id):
    try:
        course = Courses.objects.get(id=id)
        course.delete()
        messages.success(request, 'Selected Course deleted.')
    except Exception as e:
        message = traceback.format_exc()
        messages.warning(request, e)

    return redirect('admins:courses')


# Student
def StudentView(request):
    try:
        users = Users.objects.get(id=request.session['user_id'])
        students = Users.objects.filter(user_role_id=roles_std).all()
        return render(request, "admins/students.html", {'students': students, 'user': users})
    except Exception as e:
        messages.warning(request, e)


@unauthenticated_user
def StudentDetailView(request, id):
    users = Users.objects.get(id=request.session['user_id'])
    students = Users.objects.get(id=id)
    enrolls = Enrolls.objects.filter(user_id=students)
    fees_paid = FeesPayment.objects.filter(paid_from=students)
    enroll_course = Enrolls.objects.all().filter(user_id=students).values_list('course_id', flat=True).distinct()

    total_paid = 0
    for elem in fees_paid:
        total_paid += elem.paid_amount

    enroll_free = []
    for elem in enroll_course:
      if FeesPayment.objects.filter(paid_from=students, course_id=elem).exists():
            pass
      else:
            course = Courses.objects.get(id=elem)
            enroll_free.append(course)

    return render(request, 'admins/view_students.html', {'students': students, 'user': users,
                                                           'enrolls': enrolls, 'total_paid': total_paid,
                                                           'fees_paid': fees_paid, 'enroll_data': zip(enrolls, fees_paid),
                                                            'enroll_free': enroll_free
                                                           })


@unauthenticated_user
def StudentPaymentDetailView(request, course_id, id):
    users = Users.objects.get(id=request.session['user_id'])
    users_id = Users.objects.get(id=id)
    fees_paid = FeesPayment.objects.filter(course_id=course_id, paid_from=users_id)
    paid_to = []
    if fees_paid:
        paid_to = Users.objects.get(id=fees_paid[0].paid_to)
    return render(request, 'admins/view_payment_details.html', {'user': users, 'fees_paid': fees_paid, 'paid_to': paid_to.name})


@unauthenticated_user
def StudentByCourseView(request, course_id):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.get(id=course_id)
    enroll_students = Enrolls.objects.filter(course_id=courses)
    return render(request, 'admins/view_student_by_course.html', {'students': enroll_students, 'courses': courses,
                                                                    'user': users})


# Teacher
def TeacherView(request):
    teachers = Users.objects.filter(user_role_id=roles_teacher).all()
    users = Users.objects.get(id=request.session['user_id'])
    return render(request, "admins/teacher.html", {'teachers': teachers, 'user': users})


@unauthenticated_user
def TeacherDetailView(request,  id):
    users = Users.objects.get(id=request.session['user_id'])
    teacher = Users.objects.get(id=id)
    enrolls = Enrolls.objects.filter(teacher_id=id)
    enroll_students = Enrolls.objects.all().filter(teacher_id=id).values_list('user_id', flat=True).distinct()
    users = Users.objects.all()

    students_data = []
    for elem in users:
        for v in enroll_students:
            if v == elem.id:
                enroll = Enrolls.objects.filter(user_id=v)[0]
                students_data.append(enroll)

    return render(request, 'admins/view_teachers.html', {'teacher': teacher, 'user': users,
                                                           'enrolls': students_data, 'total_students': len(students_data),
                                                           })


@unauthenticated_user
def DurationView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.filter(user_id=users)
    duration = Duration.objects.all()
    duration_data = []
    for elem in courses:
        for v in duration:
            if v.course_id.id == elem.id:
                duration_data.append(v)
    return render(request, 'admins/duration.html', {'durations': duration_data, 'user': users} )


@unauthenticated_user
def DurationViewAll(request):
    users = Users.objects.get(id=request.session['user_id'])
    duration = Duration.objects.all()
    return render(request, 'admins/view_all_duration.html', {'durations': duration, 'user': users}, )


@unauthenticated_user
def DurationCreateView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.filter(user_id=users)
    if request.method == "POST":

        duration_time = CheckLength(request.POST.get('hour')) + 'h ' \
                        + CheckLength(request.POST.get('minute')) + 'm '\
                        + CheckLength(request.POST.get('second')) + "s"
        if request.POST.get('course_id') == 'Select a course':
            messages.warning(request, 'Please select the course.')
            return render(request, "admins/add_duration.html", {'courses': courses})

        course = Courses.objects.get(id=request.POST.get('course_id'))
        duration = Duration(duration_time=duration_time, course_id=course)
        try:
            new = Duration.objects.filter(course_id=course)
            if new.exists():
                messages.error(request, 'Duration already added for the selected course.')
            else:
                duration.save()
                messages.success(request, 'Duration has been added successfully.')
            return redirect('admins:duration')
        except:
            pass
    return render(request, "admins/add_duration.html", {'courses': courses})


def CheckLength(time):
    _time = time
    if len(time) == 0:
        return '00'
    elif len(time) != 2:
        return '0' + time
    return time


@unauthenticated_user
def DurationUpdateView(request,id):
    duration = Duration.objects.get(id=id)
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.all()

    if request.method == "POST":
        duration_time = CheckLength(request.POST.get('hour')) + 'h ' \
                        + CheckLength(request.POST.get('minute')) + 'm ' \
                        + CheckLength(request.POST.get('second')) + "s"

        duration.duration_time = duration_time
        duration.save()
        messages.success(request, 'Duration has been added successfully.')
        return redirect('admins:duration')

    return render(request, "admins/edit_duration.html", {'duration': duration,
                                                           'hour': int(str(duration.duration_time)[:2]),
                                                           'minute': int(str(duration.duration_time)[4:6]),
                                                           'second': int(str(duration.duration_time)[8:10]),
                                                           'courses': courses})


@unauthenticated_user
def DeleteDurationView(request, id):
    durations = Duration.objects.get(id=id)
    durations.delete()
    messages.success(request, 'Selected duration deleted.')
    return redirect('admins:duration')


@unauthenticated_user
def FeesView(request):
    try:
        users = Users.objects.get(id=request.session['user_id'])
        courses = Courses.objects.filter(user_id=users)
        fees = Fees.objects.all()
        fees_data = []

        for elem in courses:
            for v in fees:
                if v.course_id.id == elem.id:
                    fees_data.append(v)

        return render(request, 'admins/fees.html', {'courses': courses, 'fees': fees_data, 'user': users})
    except Exception as e:
        messages.warning(request, e)


@unauthenticated_user
def FeesViewAll(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.filter(user_id=users)
    fees = Fees.objects.all()

    return render(request, 'admins/fees.html', {'courses': courses, 'fees': fees, 'user': users})


@unauthenticated_user
def FeesCreateView(request):
    form = FeesForm()
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.filter(user_id=users)
    if request.method == "POST":
        form = FeesForm(request.POST)
        course_id = request.POST.get('course_id')
        if course_id == 'Select a course':
            messages.warning(request, 'Please select the course.')
            return render(request, "admins/add_fees.html", {'courses': courses, 'form': form, 'user': users})

        course = Courses.objects.get(id=course_id)
        price = request.POST.get('price')
        discount_percentage = request.POST.get('discount_percentage')
        discount_amount = request.POST.get('discount_amount')
        is_free = request.POST.get('is_free')

        # if discount_percentage is not None:
        if discount_amount == '':
            # discount_amount = str(calculateDiscount(price, discount_percentage))
            discount_percentage = None

        if price == '':
            price = 0

        if is_free is None:
            is_free = False
        else:
            is_free = True

        fees = Fees(course_id=course,
                    price=price,
                    # discount_percentage=float(str(discount_percentage)),
                    discount_percentage=discount_percentage,
                    discount_amount=discount_amount,
                    is_free=is_free,
                    )
        if form.is_valid:
            # try:
                new = Fees.objects.filter(course_id=course)
                if new.exists():
                    messages.error(request, 'Fees already added for the selected course.')
                else:
                    fees.save()
                    messages.success(request, 'Fees has been added successfully.')
                return redirect('admins:fees')
            # except:
            #     pass
    return render(request, "admins/add_fees.html", {'courses': courses, 'form': form, 'user':users})


def FeesUpdateView(request, id):
    user = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.filter(user_id=user)
    fees = Fees.objects.get(id=id)
    form = FeesForm(instance=fees)
    if request.method == "POST":
        form = FeesForm(request.POST, instance=fees)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, 'Course has been added successfully.')
                return redirect('admins:fees')
            except:
                pass
    return render(request, "admins/edit_fees.html",
                  {'form': form, 'courseId': fees.course_id.id, 'user': user, 'courses': courses})


@unauthenticated_user
def FeesDeleteView(request, id):
    fees = Fees.objects.get(id=id)
    fees.delete()
    messages.success(request, 'Selected Fee deleted.')
    return redirect('admins:fees')


def calculateDiscount(price, discount=0):
            numVal1 = price
            numVal2 = discount / 100
            totalValue = numVal1 - (numVal1 * numVal2)
            return totalValue


@unauthenticated_user
def ResourceView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.filter(user_id=users)
    return render(request, 'admins/resources.html', {'courses': courses, 'user': users})


@unauthenticated_user
def ResourceViewAll(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.filter()
    return render(request, 'admins/view_all_resources.html', {'courses': courses, 'user': users})


@unauthenticated_user
def ResourceCourseView(request, courseId):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.filter(id=courseId)
    resource = Resources.objects.filter(course_id=courseId)
    return render(request, 'admins/course_resources.html', {'courses': courses, 'resource': resource, 'user': users})


@unauthenticated_user
def ResourceCourseCreateView(request, courseId):
    users = Users.objects.get(id=request.session['user_id'])
    ALLOWED_TYPES = ['jpg', 'jpeg', 'png', 'pdf', 'mp4']

    if request.method == "POST":
        courses_instance = Courses.objects.get(id=courseId)
        form = CourseResourceForm(request.POST, request.FILES)
        resource_file = request.FILES['resource']

        if not resource_file:
            messages.error(request, 'Missing resource file')
        try:
            extension = os.path.splitext(resource_file.name)[1][1:].lower()
            if extension in ALLOWED_TYPES:
                if form.is_valid:
                    try:
                        resource = Resources(
                            resource_title=request.POST.get('resource_title'),
                            resource_description=request.POST.get('resource_description'),
                            course_id=courses_instance,
                            resource=request.FILES['resource'],
                            resource_type=extension
                        )
                        resource.save()
                        messages.success(request, 'Resource has been added successfully.')
                        return redirect('teachers:course_resources', courseId=courseId)
                    except:
                        pass
            else:
                messages.error(request, 'File types is not allowed. Only Jpg, png and pdf is allowed')
        except Exception as e:
            messages.error(request, e)
            # messages.error(request, 'Can not identify file type')

    form = CourseResourceForm()
    return render(request, "admins/add_resources.html", {'form': form, 'courseId': courseId, 'user': users})


@unauthenticated_user
def ResourceCourseUpdateView(request, id):
    users = Users.objects.get(id=request.session['user_id'])
    resource = Resources.objects.get(id=id)
    form = CourseResourceForm(instance=resource)
    if request.method == "POST":
        form = CourseResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, 'Course has been added successfully.')
                return redirect('admins:course_resources', courseId=resource.course_id.id)
            except:
                pass
    return render(request, "admins/edit_resources.html", {'form': form,  'courseId': resource.course_id.id, 'user': users})


@unauthenticated_user
def ResourceCourseDeleteView(request, id):
    resource = Resources.objects.get(id=id)
    courseId = resource.course_id.id
    resource.delete()
    messages.success(request, 'Selected resource deleted.')
    return redirect('admins:course_resources', courseId=courseId)


@unauthenticated_user
def AccountUpdateView(request):
    users = Users.objects.get(id=request.session['user_id'])
    form = UserEditForm(instance=users)
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=users)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, 'Your profile has been edited successfully.')
                return redirect('admins:dashboard')
            except:
                pass

    return render(request, "admins/edit_account.html", {'form': form, 'user': users})


@unauthenticated_user
def TestView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.filter(user_id=users)
    return render(request, 'admins/test.html', {'courses': courses, 'user': users})


@unauthenticated_user
def TestViewAll(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = Courses.objects.all()
    return render(request, 'admins/test.html', {'courses': courses, 'user': users})


@unauthenticated_user
def TestCourseView(request, courseId):
    courses = Courses.objects.filter(id=courseId)
    users = Users.objects.get(id=request.session['user_id'])
    test = Tests.objects.filter(course_id=courseId)
    return render(request, 'admins/course_test.html', {'courses': courses, 'tests': test, 'user': users})


@unauthenticated_user
def TestQuestionCreateView(request, courseId):
    if request.method == "POST":
        courses_instance = Courses.objects.get(id=courseId)
        form = CourseQuestionForm(request.POST)
        test = Tests(
            course_id=courses_instance,
            question=request.POST.get('question'),
            option1=request.POST.get('option1'),
            option2=request.POST.get('option2'),
            option3=request.POST.get('option3'),
            option4=request.POST.get('option4'),
            option5=request.POST.get('option5'),
            correct=request.POST.get('correct'),
        )
        if form.is_valid:
            try:
                test.save()
                messages.success(request, 'Question has been created successfully.')
                return redirect('admins:course_tests', courseId=courseId)
            except:
                pass

    form = CourseQuestionForm()
    return render(request, "admins/add_tests.html", {'form': form, 'courseId': courseId})


@unauthenticated_user
def TestsCourseUpdateView(request, id):
    tests = Tests.objects.get(id=id)
    form = CourseQuestionForm(instance=tests)
    if request.method == "POST":
        form = CourseQuestionForm(request.POST, request.FILES, instance=tests)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, 'Course has been updated successfully.')
                return redirect('admins:course_tests', courseId=tests.course_id.id)
            except:
                pass
    return render(request, "admins/edit_tests.html", {'form': form,  'courseId': tests.course_id.id})


@unauthenticated_user
def TestCourseDeleteView(request, id):
    tests = Tests.objects.get(id=id)
    courseId = tests.course_id.id
    tests.delete()
    messages.success(request, 'Selected resource deleted.')
    return redirect('admins:course_test', courseId=courseId)


def SearchResultView(request):
    user = Users.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        search_text = request.POST.get('search')
        courses = Courses.objects.filter((Q(course_title__icontains=search_text)
                                        | Q(code__icontains=search_text)))

        context = {"courses": courses, "search_text": search_text, "course_count": courses.count(), 'user': user}

    return render(request, "admins/search_result.html", context)



def ChangePasswordView(request):
    user = Users.objects.get(id=request.session['user_id'])
    form = ChangePasswordForm()
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        retype_password = request.POST.get('retype_password')
        check_pwd = check_password(old_password, user.password)

        if old_password == '' or new_password == '' or retype_password =='':
            messages.error(request, 'All fields are mandatory.')
        elif check_pwd == False:
            messages.error(request, 'Your entered password with old password doesn\'t match.')
        elif new_password != retype_password:
            messages.error(request, 'Your retype password is not match with new password.')
        else:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Your password is changed successfully.')
            redirect('admins:dashboard')
    return render(request, "admins/change_password.html", {"form": form,  'user': user})


@unauthenticated_user
def UserUpdateView(request, user_id):
    users = Users.objects.get(id=user_id)
    form = UserEditForm(instance=users)
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=users)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, 'Your profile has been edited successfully.')
                return redirect('admins:dashboard')
            except:
                pass

    return render(request, "admins/edit_account.html", {'form': form,})


@unauthenticated_user
def UserDeleteView(request, user_id, check_user):
    user = Users.objects.get(id=user_id)
    user.delete()
    messages.success(request, 'Selected user is deleted .')
    if check_user == 1:
        return redirect('admins:student')
    return redirect('admins:teacher')

