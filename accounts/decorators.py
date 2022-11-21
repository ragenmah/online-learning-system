from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_function):
    def wrapper_func(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('/')
        else:
            # if 'teacher_login' in request.session:
            #     return redirect('teachers:dashboard')
            # else:
            #     # if 'student_login' in request.session:
            #     return redirect('students:dashboard')
            # else:
            return view_function(request, *args, **kwargs)
    return wrapper_func
