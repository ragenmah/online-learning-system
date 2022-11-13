from django.shortcuts import render,redirect
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView
from .forms import RolesForm,CourseForm
from accounts.models import Roles,Users
from django.contrib import messages
from OnlineLearning import views

roles_std = Roles.objects.get(role_title='student').id
roles_teacher = Roles.objects.get(role_title='teacher').id

def DashboardView(request):
    return render(request, "admins/dashboard.html", views.AllContextItems(request))

# Roles
def RolesView(request):
    roles = Roles.objects.all()
    return render(request, "admins/roles.html", {'roles': roles})

def RolesCreateView(request):
    if request.method=="POST":
        form= RolesForm(request.POST)
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
    return render(request, "admins/add_roles.html",{'form':form})


def RolesDeleteView(request,id):
        role=Roles.objects.get(id=id)
        role.delete()
        roles = Roles.objects.all()

        messages.success(request, 'Selected role is deleted .')
        return render(request,'admins/roles.html',{'roles': roles})

def RolesEditView(request,id):
        roles = Roles.objects.get(id=id)
        return render(request, 'admins/edit_roles.html', {'roles': roles})


def RolesUpdateView(request, id):
    roles = Roles.objects.get(id=id)
    form = RolesForm(request.POST,instance=roles)

    if form.is_valid:
        form.save()
        messages.success(request, 'Selected role is edited .')
        return render(request, "admins/roles.html", {'roles': roles})
    return render(request, 'admins/edit_roles.html', {'roles': roles})
# end roles

# Courses
def CourseView(request):
    roles = Roles.objects.all()
    return render(request, "admins/courses.html", {'roles': roles})

def CourseCreateView(request):

    if request.method=="POST":
        form= CourseForm(request.POST)
        if form.is_valid:
            try:
                new = Roles.objects.filter(role_title=form['role_title'].value())
                if new.exists():
                    messages.error(request, 'Selected role already added.')
                    return render(request, 'admins/add_courses.html', {'form': RolesForm(request.GET)})

                else:form.save()
                messages.success(request, 'Role added successfully.')
            except:
                pass
    form = CourseForm()
    return render(request, "admins/add_courses.html",{'form':form})


# Student
def StudentView(request):
    students_id = Users.objects.filter(user_role_id=roles_std).values_list('name', flat=True)
    print(roles_std);
    students = Users.objects.filter(user_role_id=roles_std).all()
    print(students)
    # roles = Roles.objects.all()
    return render(request, "admins/students.html", {'students': students})

# Teacher
def TeacherView(request):
    teachers = Users.objects.filter(user_role_id=roles_teacher).all()

    return render(request, "admins/teacher.html", {'teachers': teachers})

