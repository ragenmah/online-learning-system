from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CourseForm
from accounts.models import Users, Courses as CourseModel, Duration
from OnlineLearning import views


def DashboardView(request):
    return render(request, "teachers/dashboard.html", views.AllContextItems(request))

def StudentView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = users.objects.filter(user_id=users)
    return render(request, 'teachers/courses.html', {'courses': courses})


def CourseView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    return render(request, 'teachers/courses.html', {'courses': courses})


def CourseCreateView(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        users = Users.objects.get(id=request.session['user_id'])
        course = CourseModel(
            code=request.POST.get('code'),
            course_title=request.POST.get('course_title'),
            course_description=request.POST.get('course_description'),
            user_id=users)
        if form.is_valid:
            try:
                new = CourseModel.objects.filter(course_title=request.POST.get('course_title'), user_id=users)
                if new.exists():
                    messages.error(request, 'The courses already added.')
                else:
                    course.save()
                    messages.success(request, 'Course has been added successfully.')
                return redirect('teachers:courses')
            except:
                pass
    form = CourseForm()
    return render(request, "teachers/add_courses.html", {'form': form})


def CourseUpdateView(request, id):
    course = CourseModel.objects.get(id=id)
    form = CourseForm(instance=course)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, 'Course has been added successfully.')
                return redirect('teachers:courses')
            except:
                pass
    return render(request, "teachers/edit_courses.html", {'form': form})


def CourseDeleteView(request, id):
    course = CourseModel.objects.get(id=id)
    course.delete()
    messages.success(request, 'Selected Course deleted.')
    return redirect('teachers:courses')


def DurationView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    print(users)
    print(courses)
    # duration = Duration.objects.filter(course_id=courses)
    duration = Duration.objects.all().select_related('course_id')
    # Duration.objects.all().prefetch_related('course_id')

    print(duration.query)
    print(duration)
    # print(duration)
    return render(request, 'teachers/duration.html', {'durations': duration})


def DurationCreateView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    if request.method == "POST":
        duration_time = request.POST.get('hour') + 'h ' + request.POST.get('minute') + 'm ' + request.POST.get(
            'second') + "s"
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


def FeesView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    return render(request, 'teachers/fees.html', {'courses': courses})


def FeesCreateView(request):
    users = Users.objects.get(id=request.session['user_id'])
    courses = CourseModel.objects.filter(user_id=users)
    if request.method == "POST":
        duration_time = request.POST.get('hour') + 'h ' + request.POST.get('minute') + 'm ' + request.POST.get(
            'second') + "s"
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
    return render(request, "teachers/add_fees.html", {'courses': courses})
