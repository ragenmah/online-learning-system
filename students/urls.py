from django.urls import include, path
from .views import DashboardView
from . import views


app_name = 'students'

urlpatterns = [
    path('', DashboardView, name='dashboard'),

    path('profile/edit', views.AccountUpdateView, name='edit_account'),

    path('courses', views.CoursesView, name='courses'),

    path('course_detail/<int:id>', views.CourseDetailView, name='course_detail'),
    path('course_enroll/<int:id>', views.CourseEnrollView, name='course_enroll'),
    path('course_unroll/<int:id>', views.CourseUnrollView, name='course_unroll'),

    path('payments/<int:id>', views.PaymentView, name='payments'),

    path('tests', views.TestView, name='tests'),
    path('tests/<int:courseId>', views.CourseTestView, name='course_test'),

]