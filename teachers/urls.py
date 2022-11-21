from django.conf.urls.static import static
from django.urls import include, path
from django.conf import settings
from .views import DashboardView
from . import  views

app_name = 'teachers'

urlpatterns = [
    path('', DashboardView, name='dashboard'),

    path('profile/edit', views.AccountUpdateView, name='edit_account'),

    path('students', views.StudentView, name='students'),
    path('students/view/<int:id>', views.StudentDetailView, name='view_student'),
    path('students/view_by_course/<int:course_id>', views.StudentByCourseView, name='view_student_by_course'),

    path('courses', views.CourseView, name='courses'),
    path('courses/add', views.CourseCreateView, name='add_courses'),
    path('courses/update/<int:id>', views.CourseUpdateView, name='update_courses'),
    path('courses/delete/<int:id>', views.CourseDeleteView, name='delete_courses'),

    path('duration', views.DurationView, name='duration'),
    path('duration/add', views.DurationCreateView, name='add_duration'),
    path('duration/update/<int:id>', views.DurationUpdateView, name='update_duration'),
    path('duration/delete/<int:id>', views.DeleteDurationView, name='delete_duration'),
    # path('courses/update/<int:id>', views.CourseUpdateView, name='update_courses'),
    # path('courses/delete/<int:id>', views.CourseDeleteView, name='delete_courses'),

    path('fees', views.FeesView, name='fees'),
    path('fees/add', views.FeesCreateView, name='add_fees'),
    path('fees/update/<int:id>', views.FeesUpdateView, name='update_fees'),
    path('fees/delete/<int:id>', views.FeesDeleteView, name='delete_fees'),

    path('resources', views.ResourceView, name='resources'),
    path('resources/course/<int:courseId>', views.ResourceCourseView, name='course_resources'),
    path('resources/course/add/<int:courseId>', views.ResourceCourseCreateView, name='add_resources'),
    path('resources/course/update/<int:id>', views.ResourceCourseUpdateView, name='update_resources'),
    path('resources/course/delete/<int:id>', views.ResourceCourseDeleteView, name='delete_resource'),

    path('test', views.TestView, name='tests'),
    path('test/course/<int:courseId>', views.TestCourseView, name='course_tests'),
    path('test/course/add/<int:courseId>', views.TestQuestionCreateView, name='add_tests'),
    path('test/course/update/<int:id>', views.TestsCourseUpdateView, name='update_tests'),
    path('test/course/delete/<int:id>', views.TestCourseDeleteView, name='delete_tests'),

]

