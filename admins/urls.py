from django.urls import include, path
from .views import DashboardView,RolesView,RolesCreateView,RolesDeleteView,RolesEditView,RolesUpdateView
from . import views
app_name = 'admins'

urlpatterns = [
    path('', DashboardView, name='dashboard'),

    path('profile/edit', views.AccountUpdateView, name='edit_account'),

    path('user/update/<int:user_id>', views.UserUpdateView, name='edit_users'),
    path('user/delete/<int:user_id>', views.UserDeleteView, name='delete_users'),

    path('change_pass', views.ChangePasswordView, name='change_password'),

    path('search', views.SearchResultView, name='search'),

    path('roles/', RolesView, name='roles'),
    path('roles/add/', RolesCreateView, name='add_roles'),
    path('roles/delete/<int:id>', RolesDeleteView, name='delete_roles'),
    path('roles/edit/<int:id>', RolesEditView, name='edit_roles'),
    path('roles/update/<int:id>', RolesUpdateView, name='update_roles'),

    path('courses/', views.CourseView, name='courses'),
    path('courses/add', views.CourseCreateView, name='add_courses'),
    path('courses/update/<int:id>', views.CourseUpdateView, name='update_courses'),
    path('courses/delete/<int:id>', views.CourseDeleteView, name='delete_courses'),
    path('courses/all', views.CourseViewAll, name='view_all_courses'),

    path('students/', views.StudentView, name='student'),
    path('students/view/<int:id>', views.StudentDetailView, name='view_student'),
    path('students/view/payment/<int:course_id>/<int:id>', views.StudentPaymentDetailView, name='view_student_payment'),
    path('students/view_by_course/<int:course_id>', views.StudentByCourseView, name='view_student_by_course'),

    path('teachers/', views.TeacherView, name='teacher'),
    path('teacher/view/<int:id>', views.TeacherDetailView, name='view_teacher'),

    path('duration', views.DurationView, name='duration'),
    path('duration/add', views.DurationCreateView, name='add_duration'),
    path('duration/update/<int:id>', views.DurationUpdateView, name='update_duration'),
    path('duration/delete/<int:id>', views.DeleteDurationView, name='delete_duration'),
    path('duration/all', views.DurationViewAll, name='view_all_duration'),

    path('fees', views.FeesView, name='fees'),
    path('fees/add', views.FeesCreateView, name='add_fees'),
    path('fees/update/<int:id>', views.FeesUpdateView, name='update_fees'),
    path('fees/delete/<int:id>', views.FeesDeleteView, name='delete_fees'),
    path('fees/all', views.FeesViewAll, name='view_all_fees'),

    path('resources', views.ResourceView, name='resources'),
    path('resources/course/<int:courseId>', views.ResourceCourseView, name='course_resources'),
    path('resources/course/add/<int:courseId>', views.ResourceCourseCreateView, name='add_resources'),
    path('resources/course/update/<int:id>', views.ResourceCourseUpdateView, name='update_resources'),
    path('resources/course/delete/<int:id>', views.ResourceCourseDeleteView, name='delete_resource'),
    path('resources/all', views.ResourceViewAll, name='view_all_resources'),

    path('test', views.TestView, name='tests'),
    path('test/course/<int:courseId>', views.TestCourseView, name='course_tests'),
    path('test/course/add/<int:courseId>', views.TestQuestionCreateView, name='add_tests'),
    path('test/course/update/<int:id>', views.TestsCourseUpdateView, name='update_tests'),
    path('test/course/delete/<int:id>', views.TestCourseDeleteView, name='delete_tests'),
    path('tes/all', views.TestViewAll, name='view_all_tests'),

]
