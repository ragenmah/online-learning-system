from django.urls import include, path
from .views import DashboardView
from . import views

app_name = 'students'

urlpatterns = [
    path('', DashboardView, name='dashboard'),
    path('course_detail', views.CourseDetailView, name='course_detail'),

]