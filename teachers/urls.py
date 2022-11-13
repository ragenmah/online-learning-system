from django.urls import include, path
from .views import DashboardView
from . import  views

app_name = 'teachers'

urlpatterns = [
    path('', DashboardView, name='dashboard'),

    path('courses', views.CourseView, name='courses'),
    path('courses/add', views.CourseCreateView, name='add_courses'),
    path('courses/update/<int:id>', views.CourseUpdateView, name='update_courses'),
    path('courses/delete/<int:id>', views.CourseDeleteView, name='delete_courses'),

    path('duration', views.DurationView, name='duration'),
    path('duration/add', views.DurationCreateView, name='add_duration'),
    # path('courses/update/<int:id>', views.CourseUpdateView, name='update_courses'),
    # path('courses/delete/<int:id>', views.CourseDeleteView, name='delete_courses'),

    path('fees', views.FeesView, name='fees'),
    path('fees/add', views.FeesCreateView, name='add_fees'),

]
