from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import IndexView,TeacherCreateView,StudentCreateView,LoginView,LogoutView


app_name = 'accounts'

urlpatterns = [
    # path('', IndexView.as_view(), name='signup'),
    path('login/', LoginView,name='login'),
    path('logout/', LogoutView, name='logout'),
    path('signup/student/', StudentCreateView, name='student_signup'),
    path('signup/teacher/', TeacherCreateView, name='teacher_signup'),

]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
