from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.views.generic import TemplateView, CreateView, ListView

from accounts.forms import UserForm
from .models import Roles,Users
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages


# Create your views here.

roles_std = Roles.objects.get(role_title='student').id
roles_teacher = Roles.objects.get(role_title='teacher').id


class IndexView(TemplateView):
    template_name = "accounts/index.html"


def TeacherCreateView(request):
        form = UserForm()
        context = {'form': form}
        if request.method == "POST":

            roles = Roles.objects.get(role_title='teacher')
            # SaveUser(roles, request, context, "accounts/teacher_signup.html", 'teachers:dashboard')
            user_role_id = roles
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            dob = request.POST.get('dob_year') + '-' + request.POST.get('dob_month') + "-" + request.POST.get('dob_day')

            contact_no = request.POST.get('contact_no')
            password = make_password(request.POST.get('password'))

            user = Users(user_role_id=user_role_id, name=name, email=email,
                         address=address, dob=dob, contact_no=contact_no, password=password)
            email_role = Users.objects.filter(email=request.POST.get('email'), user_role_id=user_role_id)

            if email_role.exists():
                messages.error(request, 'The user with this email already exist.')
                return render(request, "accounts/teacher_signup.html", context)
            else:
                user.save()
                request.session['user_id'] = Users.objects.latest('id').id
                request.session['roles_std'] = roles_std
                request.session['roles_teacher'] = roles_teacher
                messages.success(request, 'Welcome ' + name)
                return redirect('teachers:dashboard')

        return render(request, "accounts/teacher_signup.html",context)


def StudentCreateView(request):
    form = UserForm()
    context = {'form': form}
    if request.method == "POST":
        roles = Roles.objects.get(role_title='student')
        # SaveUser(roles, request, context, "accounts/teacher_signup.html", 'students:dashboard')
        user_role_id = roles
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        dob = request.POST.get('dob_year') + '-' + request.POST.get('dob_month') + "-" + request.POST.get('dob_day')

        contact_no = request.POST.get('contact_no')
        password = make_password(request.POST.get('password'))

        user = Users(user_role_id=user_role_id, name=name, email=email,
                     address=address, dob=dob, contact_no=contact_no, password=password)
        email_role = Users.objects.filter(email=request.POST.get('email'), user_role_id=user_role_id)

        if email_role.exists():
            messages.error(request, 'The user with this email already exist.')
            return render(request, "accounts/student_signup.html", context)
        else:
            user.save()
            request.session['user_id'] = Users.objects.latest('id').id
            request.session['roles_std'] = roles_std
            request.session['roles_teacher'] = roles_teacher

            messages.success(request, 'Welcome ' + name)
            return redirect('students:dashboard')

    return render(request, "accounts/student_signup.html", context)


# register users -> student and teacher ...this is not used
def SaveUser(roles, request,context,urlName,redirectTo):
    user_role_id = roles
    name = request.POST.get('name')
    email = request.POST.get('email')
    address = request.POST.get('address')
    dob = request.POST.get('dob_year') + '-' + request.POST.get('dob_month') + "-" + request.POST.get('dob_day')

    contact_no = request.POST.get('contact_no')
    password = make_password(request.POST.get('password'))

    user = Users(user_role_id=user_role_id, name=name, email=email,
                 address=address, dob=dob, contact_no=contact_no, password=password)
    email_role = Users.objects.filter(email=request.POST.get('email'), user_role_id=user_role_id)

    if email_role.exists():
        messages.error(request, 'The user with this email already exist.')
        return render(request, urlName, context)
    else:
        user.save()
        request.session['user_id'] = Users.objects.latest('id').id
        request.session['roles_std'] = roles_std
        request.session['roles_teacher'] = roles_teacher

        messages.success(request, 'Welcome ' + name)
        return redirect(redirectTo)


def LoginView(request):
    CreateAdmin()
    if request.method == "POST":

        try:
            email = request.POST.get('email')
            user = Users.objects.get(email=email)
            check_pwd = check_password(request.POST['password'], user.password)
            roles = Roles.objects.get(id=user.user_role_id.id)
            check_email = Users.objects.filter(email=email)

            if check_email.exists():
                pass
            else:
                messages.warning(request, 'Email not found')
                pass
            if check_pwd == False:
                messages.error(request, 'Password is incorrect')
                pass
            else:
                request.session['user_id'] = user.id
                # request.session['email']= user.email
                request.session['roles_std'] = roles_std
                request.session['roles_teacher']= roles_teacher
                messages.success(request, 'Welcome ' + user.name)

                if roles.role_title == 'teacher':
                    request.session['teacher_login'] = roles_teacher
                    return redirect('teachers:dashboard')
                if roles.role_title == 'student':
                    request.session['student_login'] = roles_std
                    return redirect('students:dashboard')
                else:
                    return redirect('admins:dashboard')
        except:
            pass
    context = {}
    return render(request, "accounts/login.html", context)


def CreateAdmin():
    new = Users.objects.filter(email='admin@admin.com')
    roles = Roles.objects.get(role_title='admin')
    if new.exists():
        pass
    else:
        user_role_id = roles
        name = 'admin'
        email = 'admin@admin.com'
        address = ''
        dob = '1998-01-01'
        contact_no = ''
        password = make_password('admin123')
        user = Users(user_role_id=user_role_id, name=name, email=email,
                     address=address, dob=dob, contact_no=contact_no, password=password)
        user.save()


def LogoutView(request):
        del request.session['user_id']
        del request.session['roles_std']
        del request.session['roles_teacher']
        if 'teacher_login' in request.session:
            del request.session['teacher_login']
        if 'student_login' in request.session:
            del request.session['student_login']
        return redirect('/')
