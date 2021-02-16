from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from account.models import *


class CustomUserAdmin(UserAdmin):
    #add_form = UserSignUpForm
    model = user


admin.site.register(user)#,CustomUserAdmin)

admin.site.register(Manager)

admin.site.register(Teacher)

admin.site.register(Student)

admin.site.register(surat)
admin.site.register(juz)
admin.site.register(hizp)
admin.site.register(ruba)
admin.site.register(aya)
admin.site.register(Absence)
admin.site.register(Degree)


admin.site.register(Lecture)

admin.site.register(Student_Lecture)