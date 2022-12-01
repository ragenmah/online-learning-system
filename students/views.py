import os

from django.shortcuts import render, redirect
from accounts.models import Roles, Users, Courses, Duration, Resources, Enrolls, Tests, Fees, FeesPayment
from accounts.forms import UserEditForm, ChangePasswordForm
from django.contrib import messages
from OnlineLearning import views
from accounts.decorators import unauthenticated_user
from datetime import date
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from PIL import Image
from django.shortcuts import get_object_or_404
today = date.today()

def check_img(filename):
    try:
        Image.open(filename)
        return True
    except IOError:
        print(filename,'corrupted')
        return False


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
    # try:
        courses = Courses.objects.get(id=id)
        duration = get_object_or_404(Duration, course_id=id)
        enrolls_total = Enrolls.objects.filter(course_id=id).count()
        fee = Fees.objects.get(course_id=courses)
        users = Users.objects.get(id=request.session['user_id'])
        is_paid = False
        check_paid = FeesPayment.objects.filter(course_id=courses, paid_from=users)
        if check_paid.exists():
            is_paid = True
        return render(request, "students/course_detail.html", {'courses': courses, 'duration': duration,
                                                                   'enrolls_total': enrolls_total, 'fees': fee,
                                                                   'user': users, 'is_paid': is_paid, })
    # except:
    #     pass



@unauthenticated_user
def CourseEnrollView(request, id):
    courses = Courses.objects.get(id=id)
    duration = Duration.objects.get(course_id=id)
    resource = Resources.objects.filter(course_id=id)
    fee = Fees.objects.get(course_id=id)
    user = Users.objects.get(id=request.session['user_id'])
    check_paid = FeesPayment.objects.filter(course_id=courses, paid_from=user)
    payment = []
    paid_fee = 0
    if check_paid.exists():
        for v in check_paid:
            payment.append(v)
    if len(payment) > 0:
        paid_fee = payment[0].paid_amount

    enrolls = Enrolls(
        course_id=courses,
        user_id=user,
        teacher_id=courses.user_id.id
    )
    payment_image = ''
    payment_mode = 'Card'

    if 'voucher_image' in request.FILES :
        payment_image = request.FILES['voucher_image']
        payment_mode = 'Bank account'
        if not check_img(payment_image):
            messages.error(request, 'The image is not supported.')
            return redirect('students:payments', id=id)

    price = fee.price

    feesPayment = FeesPayment(
        course_id=courses,
        paid_amount=price,
        payment_image=payment_image,
        payment_method=payment_mode,
        status=1,
        paid_from=user,
        paid_to=courses.user_id.id,
    )

    print("resource")
    print("resource")
    print("resource")
    print("resource")
    print(resource[0].resource_type)

    if request.method == "POST":
        # try:
            new = Enrolls.objects.filter(course_id=courses, user_id=user)
            payments = FeesPayment.objects.filter(course_id=courses, paid_from=user)
            if new.exists():
                messages.error(request, 'Selected course already enrolled.')
                return redirect('students:course_detail', id=id)
            elif payments.exists() or fee.is_free:
                enrolls.save()
                messages.success(request, 'You have successfully enrolled this subject.')
            else:
                feesPayment.save()
                enrolls.save()
                messages.success(request, 'You have successfully enrolled this subject.')
        # except:
        #     pass
    enrolls_total = Enrolls.objects.filter(course_id=id).count()
    return render(request, "students/course_enroll.html", {'courses': courses, 'duration': duration,
                                                           'resources': resource, 'enrolls_total': enrolls_total,
                                                           'fees': fee, 'user': user, "payment": paid_fee})


@unauthenticated_user
def CourseUnrollView(request, id):
    courses = Courses.objects.get(id=id)
    user = Users.objects.get(id=request.session['user_id'])
    enroll = Enrolls.objects.get(course_id=courses, user_id=user)
    enroll.delete()
    messages.success(request, 'Selected course remove from enroll.')
    return redirect("students:course_detail", id=id)


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
    duration = Duration.objects.get(course_id=courseId)
    user = Users.objects.get(id=request.session['user_id'])
    check_paid = FeesPayment.objects.filter(course_id=courses, paid_from=user)
    payment = []
    paid_fee = 0
    if check_paid.exists():
        for v in check_paid:
            payment.append(v)
    if len(payment) > 0:
        paid_fee = payment[0].paid_amount

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
        enrolls_total = Enrolls.objects.filter(course_id=courseId).count()
        context = {'duration': duration, 'enrolls_total': enrolls_total, 'questions': questions, 'courses': courses,
                   'tests': test, 'user': user, "payment": paid_fee}

    return render(request, "students/course_test.html", context)


def SearchResultView(request):
    user = Users.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        search_text = request.POST.get('search')
        # course = Courses.objects.get(Q( title__icontains=search_text) & Q(content__icontains=search_text))

        courses = Courses.objects.filter(Q(course_title__icontains=search_text)
                                    | Q(code__icontains=search_text))
        fees = Fees.objects.all()

        fees_data = []
        for elem in courses:
            for v in fees:
                if v.course_id.id == elem.id:
                    fees_data.append(v)

    return render(request, "students/search_result.html", {"fees": fees_data,
                                                           "search_text": search_text,
                                                           "course_count": len(fees_data), 'user': user
                                                           })


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
            redirect('students:dashboard')
    return render(request, "students/change_password.html", {"form": form,  'user': user})


