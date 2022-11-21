from django.shortcuts import render, redirect
from accounts.models import Roles, Users, Courses, Duration, Resources, Enrolls, Tests, Fees, FeesPayment
from accounts.forms import UserEditForm
from django.contrib import messages
from OnlineLearning import views
from accounts.decorators import unauthenticated_user
from datetime import date

today = date.today()

@unauthenticated_user
def DashboardView(request):
    return render(request, 'students/dashboard.html', views.ContextForStudents(request))

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
                return redirect('students:dashboard')
            except:
                pass

    return render(request, "students/edit_account.html", {'form': form, 'user': users})

@unauthenticated_user
def CourseDetailView(request, id):
    courses = Courses.objects.get(id=id)
    duration = Duration.objects.get(course_id=id)
    enrolls_total = Enrolls.objects.filter(course_id=id).count()
    fee = Fees.objects.get(course_id=id)
    print("fee")
    print(fee)
    print(fee)
    users = Users.objects.get(id=request.session['user_id'])
    return render(request, "students/course_detail.html", {'courses': courses, 'duration': duration,
                                                           'enrolls_total': enrolls_total, 'fees': fee,
                                                           'user': users})

@unauthenticated_user
def CourseEnrollView(request, id):
    courses = Courses.objects.get(id=id)
    duration = Duration.objects.get(course_id=id)
    resource = Resources.objects.filter(course_id=id)
    fee = Fees.objects.get(course_id=id)
    user = Users.objects.get(id=request.session['user_id'])

    enrolls = Enrolls(
        course_id=courses,
        user_id=user,
        teacher_id=courses.user_id.id
    )
    payment_image = ''
    payment_mode = 'Card'
    print(request)
    print(request)
    print(request.POST.get('voucher_image'))
    print(request)
    if 'voucher_image' in request:
        payment_image = request.POST.get('voucher_image')
        payment_mode = 'Bank account'

    feesPayment = FeesPayment(
        course_id=courses,
        Paid_amount=fee.price,
        payment_image=payment_image,
        payment_method=payment_mode,
        status=1,
        paid_from=user,
        paid_to=courses.user_id.id,
    )

    if request.method == "POST":
        # try:
            new = Enrolls.objects.filter(course_id=courses, user_id=user)
            payments = FeesPayment.objects.filter(course_id=courses, paid_from=user)
            if new.exists() & payments.exists():
                messages.error(request, 'Selected course already enrolled.')
                return redirect('students:course_detail', id=id)
            else:
                feesPayment.save()
                enrolls.save()
                messages.success(request, 'You have successfully enrolled this subject.')
        # except:
        #     pass
    enrolls_total = Enrolls.objects.filter(course_id=id).count()
    return render(request, "students/course_enroll.html", {'courses': courses, 'duration': duration,
                                                           'resources': resource, 'enrolls_total': enrolls_total,
                                                           'fees': fee, 'user': user})

@unauthenticated_user
def CourseUnrollView(request, id):
    courses = Courses.objects.get(id=id)
    duration = Duration.objects.get(course_id=id)
    user = Users.objects.get(id=request.session['user_id'])
    enroll = Enrolls.objects.get(course_id=courses, user_id=user)
    enroll.delete()
    messages.success(request, 'Selected course remove from enroll.')
    return render(request, "students/course_detail.html", {'courses': courses, 'duration': duration, })

@unauthenticated_user
def CoursesView(request):
    return render(request, "students/courses.html", views.ContextForStudents(request))

@unauthenticated_user
def TestView(request):
    return render(request, "students/test.html", views.ContextForStudents(request))

@unauthenticated_user
def PaymentView(request, id):
    courses = Courses.objects.get(id=id)
    duration = Duration.objects.get(course_id=id)
    resource = Resources.objects.filter(course_id=id)
    fee = Fees.objects.get(course_id=id)
    enrolls_total = Enrolls.objects.filter(course_id=id).count()
    user = Users.objects.get(id=request.session['user_id'])
    context = {'courses': courses,
               'duration': duration,
               'resources': resource,
               'enrolls_total': enrolls_total,
               'fees': fee,
               'user': user}
    return render(request, "students/payment.html", context)


@unauthenticated_user
def CourseTestView(request, courseId):
    courses = Courses.objects.get(id=courseId)
    test = Tests.objects.filter(course_id=courseId)
    user = Users.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        print(request.POST)
        questions = Tests.objects.filter(course_id=courseId)
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            print(request.POST.get(q.question))
            print(q.correct)
            print()
            if q.correct == request.POST.get(q.question):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score / (total * 10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total,
            'courses': courses,
            'tests': test,
            'user': user,
            'issue_date': today.strftime("%B %d, %Y"),
        }
        return render(request, 'students/certificate.html', context)
    else:
        questions = test
        context = {
            'questions': questions, 'courses': courses, 'tests': test, 'user': user
        }
    # enrolls = Enrolls.objects.filter(user_id=request.session['user_id'])

    return render(request, "students/course_test.html", context)
