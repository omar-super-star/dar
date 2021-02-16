from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts:login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def manager_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts:login'):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_manager,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def stuff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts:login'):
    '''
    Decorator for views that checks that the logged in user is a stuff,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u:  u.is_manager or u.is_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts:login'):
    '''
    Decorator for views that checks that the logged in user is a stuff,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u:  u.is_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def not_student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts:login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: not u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator