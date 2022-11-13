from django.urls import include, path
from .views import DashboardView,RolesView,RolesCreateView,RolesDeleteView,RolesEditView,RolesUpdateView
from . import views
app_name = 'admins'

urlpatterns = [
    path('', DashboardView, name='dashboard'),

    path('roles/', RolesView, name='roles'),
    path('roles/add/', RolesCreateView, name='add_roles'),
    path('roles/delete/<int:id>', RolesDeleteView, name='delete_roles'),
    path('roles/edit/<int:id>', RolesEditView, name='edit_roles'),
    path('roles/update/<int:id>', RolesUpdateView, name='update_roles'),

    path('courses/',views.CourseView,name='courses'),
    path('courses/add/', views.CourseCreateView, name='add_courses'),

    path('student/', views.StudentView, name='student'),

    path('teacher/', views.TeacherView, name='teacher'),

]
