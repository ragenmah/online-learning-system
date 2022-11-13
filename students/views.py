from django.shortcuts import render
from accounts.models import Roles,Users
from django.contrib.auth.decorators import login_required
from OnlineLearning import views



def DashboardView(request):
    return render(request, 'students/dashboard.html', views.AllContextItems(request))

def CourseDetailView(request):
    return render(request, "students/course_detail.html")
