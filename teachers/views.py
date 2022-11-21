from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CourseForm, CourseResourceForm, CourseQuestionForm, FeesForm
from accounts.forms import UserEditForm
from accounts.models import Users, Courses as CourseModel, Duration, Resources, Tests, Enrolls, Fees
from OnlineLearning import views
from accounts.decorators import unauthenticated_user

@unauthenticated_user
def DashboardView(request):
    return render(request, "teachers/dashboard.html", views.AllContextItems(request))
@unauthenticated_user
def StudentView(request):
    users = Users.objects.get(id=request.session['user_id'])
    enroll_students = Enrolls.objects.filter(teacher_id=request.session['user_id'])
    return render(request, 'teachers/students.html', {'students': enroll_students, 'user': users})
@unauthenticated_user
def StudentDetailView(request, id):
    users = Users.objects.get(id=request.session['user_id'])
    enroll_students = Enrolls.objects.get(user_id=id)
    return render(request, 'teachers/view_students.html', {'students': enroll_students, 'user': users})

@unauthenticated_user
def StudentByCourseView(request, course_id):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.get(id=course_id)
    enroll_students = Enrolls.objects.filter(course_id=courses)
    return render(request, 'teachers/view_student_by_course.html', {'students': enroll_students, 'courses': courses,
                                                                    'user': users})

@unauthenticated_user
def CourseView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    return render(request, 'teachers/courses.html', {'courses': courses,  'user': users})

@unauthenticated_user
def CourseCreateView(request):
    if request.method == "POST":
        users = Users.objects.get(id=request.session['user_id'])
        form = CourseForm(request.POST, request.FILES, instance=users)

        course = CourseModel(
            code=request.POST.get('code'),
            course_title=request.POST.get('course_title'),
            course_description=request.POST.get('course_description'),
            user_id=users,
            course_thumbnail=request.FILES['course_thumbnail']
        )
        
        if form.is_valid:
            try:
                new = CourseModel.objects.filter(course_title=request.POST.get('course_title'), user_id=users)
                if new.exists():
                    messages.error(request, 'The courses already added.')
                else:
                    course.save()
                    # img_object = form.instance
                    # print(img_object)
                    messages.success(request, 'Course has been added successfully.')
                    return redirect('teachers:courses')
            except:
                pass
    form = CourseForm()
    return render(request, "teachers/add_courses.html", {'form': form})

@unauthenticated_user
def CourseUpdateView(request, id):
    course = CourseModel.objects.get(id=id)
    form = CourseForm(instance=course)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, 'Course has been updated successfully.')
                return redirect('teachers:courses')
            except:
                pass
    return render(request, "teachers/edit_courses.html", {'form': form})

@unauthenticated_user
def CourseDeleteView(request, id):
    course = CourseModel.objects.get(id=id)
    course.delete()
    messages.success(request, 'Selected Course deleted.')
    return redirect('teachers:courses')

@unauthenticated_user
def DurationView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    print(users)
    print(courses)
    # duration = Duration.objects.filter(course_id=courses)
    duration = Duration.objects.all()
        # Duration.objects.all().select_related('course_id')
    print(duration.query)
    print(duration)
    # print(duration)
    return render(request, 'teachers/duration.html', {'durations': duration, 'courses': courses, 'user': users}, )

@unauthenticated_user
def DurationCreateView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    if request.method == "POST":

        duration_time = CheckLength(request.POST.get('hour')) + 'h ' \
                        + CheckLength(request.POST.get('minute')) + 'm '\
                        + CheckLength(request.POST.get('second')) + "s"
        if request.POST.get('course_id') == 'Select a course':
            messages.warning(request, 'Please select the course.')
            return render(request, "teachers/add_duration.html", {'courses': courses})

        course = CourseModel.objects.get(id=request.POST.get('course_id'))
        duration = Duration(duration_time=duration_time, course_id=course)
        try:
            new = Duration.objects.filter(course_id=course)
            if new.exists():
                messages.error(request, 'Duration already added for the selected course.')
            else:
                duration.save()
                messages.success(request, 'Duration has been added successfully.')
            return redirect('teachers:duration')
        except:
            pass
    return render(request, "teachers/add_duration.html", {'courses': courses})


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
    courses = CourseModel.objects.filter(user_id=users)
    print("duration")
    print("duration")
    print(int(str(duration.duration_time)[4:6]))
    print(int(str(duration.duration_time)[8:10]))
    print(duration.duration_time)

    if request.method == "POST":
        duration_time = CheckLength(request.POST.get('hour')) + 'h ' \
                        + CheckLength(request.POST.get('minute')) + 'm ' \
                        + CheckLength(request.POST.get('second')) + "s"
        # course = CourseModel.objects.get(id=request.POST.get('course_id'))
        # duration = Duration(duration_time=duration_time, course_id=course)

        duration.duration_time = duration_time
        duration.save()
        messages.success(request, 'Duration has been added successfully.')
        return redirect('teachers:duration')

    return render(request, "teachers/edit_duration.html", {'duration': duration,
                                                           'hour': int(str(duration.duration_time)[:2]),
                                                           'minute': int(str(duration.duration_time)[4:6]),
                                                           'second': int(str(duration.duration_time)[8:10]),
                                                           'courses': courses})

@unauthenticated_user
def DeleteDurationView(request, id):
    durations = Duration.objects.get(id=id)
    durations.delete()
    messages.success(request, 'Selected duration deleted.')
    return redirect('teachers:duration')

@unauthenticated_user
def FeesView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    # course_list = []
    # fee_list = []
    # qs = courses.values(*course_list)
    fees = Fees.objects.all()
    # fs = fees.values(*course_list)
    # user_ids = CourseModel.objects.filter(user_id=users).exclude(user_id=users).values_list('id', flat=True)
    # fees = Fees.objects.filter(course_id=user_ids)

    fees_data = []
    for elem in courses:
        for v in fees:
            if v.course_id.id == elem.id:
                fees_data.append(v)
    print(fees_data)
    return render(request, 'teachers/fees.html', {'courses': courses, 'fees': fees_data, 'user': users})

@unauthenticated_user
def FeesCreateView(request):
    form = FeesForm()
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    if request.method == "POST":
        form = FeesForm(request.POST)
        course_id = request.POST.get('course_id')
        if course_id == 'Select a course':
            messages.warning(request, 'Please select the course.')
            return render(request, "teachers/add_fees.html", {'courses': courses, 'form': form, 'user': users})

        course = CourseModel.objects.get(id=course_id)
        price = request.POST.get('price')
        discount_percentage = request.POST.get('discount_percentage')
        discountAmt = request.POST.get('discount_amount')
        if discountAmt=='':
            discountAmt= str(calculateDiscount(price, discount_percentage))

        fees = Fees( course_id=course,
                     price=price,
                     # discount_percentage=float(str(discount_percentage)),
                     discount_percentage=discount_percentage,
                     discount_amount=discountAmt,
        )
        if form.is_valid:
            try:
                new = Fees.objects.filter(course_id=course)
                if new.exists():
                    messages.error(request, 'Fees already added for the selected course.')
                else:
                    fees.save()
                    messages.success(request, 'Fees has been added successfully.')
                return redirect('teachers:fees')
            except:
                pass
    return render(request, "teachers/add_fees.html", {'courses': courses, 'form': form, 'user':users})

def FeesUpdateView(request, id):
    user = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=user)
    fees = Fees.objects.get(id=id)
    form = FeesForm(instance=fees)
    if request.method == "POST":
        form = FeesForm(request.POST, instance=fees)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, 'Course has been added successfully.')
                return redirect('teachers:fees')
            except:
                pass
    return render(request, "teachers/edit_fees.html",
                  {'form': form, 'courseId': fees.course_id.id, 'user': user, 'courses': courses})

@unauthenticated_user
def FeesDeleteView(request, id):
    fees = Fees.objects.get(id=id)
    fees.delete()
    messages.success(request, 'Selected Fee deleted.')
    return redirect('teachers:fees')

def calculateDiscount(price, discount) :
            numVal1 = price
            numVal2 = discount / 100;
            totalValue = numVal1 - (numVal1 * numVal2)
            return totalValue

@unauthenticated_user
def ResourceView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    return render(request, 'teachers/resources.html', {'courses': courses, 'user': users})

@unauthenticated_user
def ResourceCourseView(request, courseId):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(id=courseId)
    resource = Resources.objects.filter(course_id=courseId)
    return render(request, 'teachers/course_resources.html', {'courses': courses, 'resource': resource, 'user': users})

@unauthenticated_user
def ResourceCourseCreateView(request, courseId):
    users = Users.objects.get(id=request.session['user_id'])

    if request.method == "POST":
        courses_instance = CourseModel.objects.get(id=courseId)
        form = CourseResourceForm(request.POST, request.FILES)

        resource = Resources(
            resource_title=request.POST.get('resource_title'),
            resource_description=request.POST.get('resource_description'),
            course_id=courses_instance,
            resource=request.FILES['resource']
        )
        if form.is_valid:
               try:
                resource.save()
                messages.success(request, 'Resource has been added successfully.')
                return redirect('teachers:course_resources', courseId=courseId)
               except:
                   pass

    form = CourseResourceForm()
    return render(request, "teachers/add_resources.html", {'form': form, 'courseId':courseId, 'user': users})

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
                return redirect('teachers:course_resources', courseId=resource.course_id.id)
            except:
                pass
    return render(request, "teachers/edit_resources.html", {'form': form,  'courseId': resource.course_id.id, 'user': users})

@unauthenticated_user
def ResourceCourseDeleteView(request, id):
    resource = Resources.objects.get(id=id)
    courseId = resource.course_id.id
    resource.delete()
    messages.success(request, 'Selected resource deleted.')
    return redirect('teachers:course_resources', courseId=courseId)


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
                return redirect('teachers:dashboard')
            except:
                pass

    return render(request, "teachers/edit_account.html", {'form': form,})

@unauthenticated_user
def TestView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    return render(request, 'teachers/test.html', {'courses': courses})

@unauthenticated_user
def TestCourseView(request, courseId):
    courses = CourseModel.objects.filter(id=courseId)
    test = Tests.objects.filter(course_id=courseId)
    return render(request, 'teachers/course_test.html', {'courses': courses, 'tests': test})

@unauthenticated_user
def TestQuestionCreateView(request, courseId):
    if request.method == "POST":
        courses_instance = CourseModel.objects.get(id=courseId)
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
                return redirect('teachers:course_tests', courseId=courseId)
            except:
                pass

    form = CourseQuestionForm()
    return render(request, "teachers/add_tests.html", {'form': form, 'courseId': courseId})

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
                return redirect('teachers:course_tests', courseId=tests.course_id.id)
            except:
                pass
    return render(request, "teachers/edit_tests.html", {'form': form,  'courseId': tests.course_id.id})

@unauthenticated_user
def TestCourseDeleteView(request, id):
    tests = Tests.objects.get(id=id)
    courseId = tests.course_id.id
    tests.delete()
    messages.success(request, 'Selected resource deleted.')
    return redirect('teachers:course_test', courseId=courseId)
