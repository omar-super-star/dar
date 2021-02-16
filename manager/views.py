import datetime
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from account.barcodegenrator import MyBarcodeDrawing
from account.forms import UserSignUpForm
from account.models import Teacher, Student, aya, Lecture, Absence, Student_Lecture, Degree
from manager.filter import StudentFilterFormSuperUser, StudentFilterFormTeacher, \
    StudentFilterFormManager, StudentFilter
from manager.forms import LectureCreateForm, LectureCreateTeacherForm, HomeWorkDegree, StudentFormmanager
from quranproject.decrorator import manager_required, stuff_required
from teacher.views import dayoftheweek


@login_required
@manager_required
def addTeacherForm(request):
    err=request.GET.get("err","")
    return render(request,"addteacher.html",{
        'form':UserSignUpForm,
        "error":err
    })
@login_required
@manager_required
def addTeacher(request):
    user_form = UserSignUpForm(request.POST)

    if user_form.is_valid() :
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data['password2'])
        user.is_teacher=True
        user.save()
        print(request.user.is_manager)

        teacher=Teacher(user=user,manager=request.user.manager)
        teacher.save()
        return HttpResponseRedirect(reverse('manager:addteacherform')+"?statue=successed")

    else:
        return HttpResponseRedirect(reverse('manager:addteacherform')+f"?statue=falsed&&err={user_form.errors}")
@login_required
@manager_required
def showTeacher(request):
    context = {}
    num = request.GET.get("page", 1)
    objects = Teacher.objects.filter(manager=request.user.manager.id).all()
    # f = StudentgroupFilter(self.request.GET, queryset=objects)
    pages = Paginator(objects, 50)
    teachers = pages.page(num)

    '''context["name"] = request.GET.get("student__user__username", "")
    context["group"] = request.GET.get("group", "")
    context["filter_search"] = StudentgroupFilterFormManager(user1=request.user,
                                               initial={"student__user__username": context["name"],
                                                        "group": context["group"]})'''

    context['teachers'] = teachers
    context["pages"] = pages.page_range

    return render(request,"teacherlist.html",context)
@login_required
@manager_required
def teacherdetail(request,id):
    return render(request, "teacherdetail.html",{
        "teacher":Teacher.objects.filter(id=id).first()
    })



@login_required
@stuff_required
def addStudentForm(request):
    err=request.GET.get("err","")
    return render(request,"addstudent.html",{
        'form':UserSignUpForm,
        'form_student':StudentFormmanager(user1=request.user),
        "error":err
    })
@login_required
@stuff_required
def addStudent(request):
    user_form = UserSignUpForm(request.POST)
    student_form=StudentFormmanager(request.POST,user1=request.user)

    if user_form.is_valid() and student_form.save():

        while True:
            randomstring=''.join((random.choice("asdfergwqtyhujiklopnbvcxz12345678963258741") for i in range(15)))
            if (Student.objects.filter(barcode=randomstring).first() == None):
                break
        print(randomstring)
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data['password2'])
        user.is_student = True
        user.save()
        print(request.user.is_manager)

        student=student_form.save()
        student.user=user
        student.barcode=randomstring
        b = MyBarcodeDrawing(randomstring)
        b.save(formats=['jpg'], outDir='./static/barcodes/', fnRoot=f'{student.user.username}')
        student.save()

        return HttpResponseRedirect(reverse('manager:addstudentform')+"?statue=successed")
    else:
        return HttpResponseRedirect(reverse('manager:addstudentform')+f"?statue=falsed&&err={user_form.errors}")


@login_required
def showStudent(request):
    context = {}
    num = request.GET.get("page", 1)
    user=request.user
    name = request.GET.get("student__user__username", "")
    teacher = request.GET.get("teacher__id", "")
    degree = request.GET.get("degree__name", "")
    manager = request.GET.get("teacher__manager", "")
    if user.is_manager:
        objects = Student.objects.filter(teacher__manager=user.manager.id).all()
        context["filter"] = StudentFilterFormManager(user1=request.user,
                                                          initial={ "name": name,
                                                                    "teacher__id":teacher,
                                                                    "degree__name":degree,
                                                                    })
    elif user.is_teacher:
        objects = Student.objects.filter(teacher=user.teacher.id).all()
        context["filter"] = StudentFilterFormTeacher(user1=request.user,
                                                          initial={"name": name,
                                                                   "degree__name": degree,
                                                                   })

    else:
        objects = Student.objects.all()
        context["filter"] = StudentFilterFormSuperUser(user1=request.user,
                                                          initial={"name": name,
                                                                   "degree__name": degree,
                                                                   "teacher__manager":manager,
                                                                   "teacher__id":teacher
                                                                   })
    f = StudentFilter(request.GET, queryset=objects)
    pages = Paginator(f.qs,2)
    students = pages.page(num)

    context['students'] = students
    context["pages"] = pages.page_range

    return render(request,"studentlist.html",context)
@login_required
def studentdetail(request,id):

    total=Absence.objects.filter(lecture__student__id=id).all().count()
    print(total)
    notabsencetotel=Absence.objects.filter(lecture__student__id=id,absence=False).all().count()
    print(notabsencetotel)
    degree=(notabsencetotel/total)*100
    st=Student.objects.filter(id=id).first()
    if st.finishlogin != None:
        if st.finishlogin <= datetime.datetime.now():
            st.paid=False
            st.save()
    return render(request, "studentdetail.html",{
        "student":st,
        "absence":degree,

    })

@login_required
def paidstudent(request,id):
    st=Student.objects.filter(id=id).first()
    st.paidf()
    st.save()
    return JsonResponse({"id":1})



class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentFormmanager

    def form_valid(self, *args, **kwargs):
        print("post", self.request.POST)
        name = self.request.POST.get("degree")
        degree = Degree.objects.filter(name=name).first()
        self.object.degree = degree if degree != None else self.object.degree
        self.object.save()
        return redirect('teacher:updatestudentform',  self.object.id)

''' def get_success_url(self):
        success_url = 
        return success_url'''





@login_required
@stuff_required
def addLecturetForm(request):
    err=request.GET.get("err","")
    if request.user.is_manager:
        teacher_form=LectureCreateTeacherForm(teachers=Teacher.objects.filter(manager__id=request.user.manager.id).all())
    else:
        teacher_form=None
    return render(request,"addlecture.html",{
        'form_lecture':LectureCreateForm(),
        "teacher_form":teacher_form,
        "error":err
    })
@login_required
@stuff_required
def addLecture(request):
    lecture_form = LectureCreateForm(request.POST)
    hour=request.POST.get("hour","0")
    print(hour)
    teacher_id=int(request.POST.get("teacher","0"))

    if request.user.is_manager:
        if teacher_id ==0:
            return HttpResponseRedirect(reverse('manager:addlectureform') + f"?statue=falsed&&err=please enter teacher")
        teacher=Teacher.objects.filter(id=teacher_id).first()
    else:
        teacher = Teacher.objects.filter(manager__id=request.user.teacher.id).first()
    if hour==0 :
        return HttpResponseRedirect(reverse('manager:addlectureform') + f"?statue=falsed&&err=please enter hour")

    if lecture_form.is_valid() :
        H=hour.split(":")[0]
        M=hour.split(":")[1]
        time=datetime.time(int(H),int(M))
        lecture=lecture_form.save()
        lecture.hour=time
        lecture.teacher=teacher
        lecture.save()
        return HttpResponseRedirect(reverse('manager:addlectureform')+"?statue=successed")

    else:
        return HttpResponseRedirect(reverse('manager:addlectureform')+f"?statue=falsed&&err={lecture_form.errors}")

@login_required
@stuff_required
def showLecture(request):
    num = request.GET.get("page", 1)
    if request.user.is_manager:
        objects = Lecture.objects.filter(teacher__manager=request.user.manager.id).all()
    else:
        objects = Lecture.objects.filter(teacher=request.user.teacher.id).all()
    # f = StudentgroupFilter(self.request.GET, queryset=objects)
    pages = Paginator(objects, 50)
    lectures = pages.page(num)
    context = {}
    '''context["name"] = self.request.GET.get("student__user__username", "")
    context["group"] = self.request.GET.get("group", "")
    context["filter"] = StudentgroupFilterForm(user1=self.request.user,
                                               initial={"student__user__username": context["name"],
                                                        "group": context["group"]})
    '''
    context['lectures'] = lectures
    context["pages"] = pages.page_range

    return render(request,"lecturelist.html",context)

@login_required
@stuff_required
def showLectureTeacher(request,id):
    num = request.GET.get("page", 1)
    objects = Lecture.objects.filter(teacher=id).all()
    # f = StudentgroupFilter(self.request.GET, queryset=objects)
    pages = Paginator(objects, 50)
    lectures = pages.page(num)
    context = {}
    '''context["name"] = self.request.GET.get("student__user__username", "")
    context["group"] = self.request.GET.get("group", "")
    context["filter"] = StudentgroupFilterForm(user1=self.request.user,
                                               initial={"student__user__username": context["name"],
                                                        "group": context["group"]})
    '''
    context['lectures'] = lectures
    context["pages"] = pages.page_range

    return render(request,"lecturelist.html",context)

@login_required
@manager_required
def showStudentTeacher(request,id):
    num = request.GET.get("page", 1)
    objects = Student.objects.filter(teacher=id).all()
    # f = StudentgroupFilter(self.request.GET, queryset=objects)
    pages = Paginator(objects, 50)
    students = pages.page(num)
    context = {}
    '''context["name"] = self.request.GET.get("student__user__username", "")
    context["group"] = self.request.GET.get("group", "")
    context["filter"] = StudentgroupFilterForm(user1=self.request.user,
                                               initial={"student__user__username": context["name"],
                                                        "group": context["group"]})
    '''
    context['students'] = students
    context["pages"] = pages.page_range

    return render(request,"studentlist.html",context)

@login_required
@stuff_required
def lecturedetail(request,id):
    return render(request, "lecturedetail.html",{
        "lecture":Lecture.objects.filter(id=id).first()
    })

@login_required
@stuff_required
def showStudentLecture(request,id):
    num = request.GET.get("page", 1)
    objects = Student.objects.filter(student_lecture__lecture__id=id).all()
    # f = StudentgroupFilter(self.request.GET, queryset=objects)
    pages = Paginator(objects, 50)
    students = pages.page(num)
    context = {}
    '''context["name"] = self.request.GET.get("student__user__username", "")
    context["group"] = self.request.GET.get("group", "")
    context["filter"] = StudentgroupFilterForm(user1=self.request.user,
                                               initial={"student__user__username": context["name"],
                                                        "group": context["group"]})
    '''
    context['students'] = students
    context["pages"] = pages.page_range

    return render(request, "studentlist.html", context)

@login_required
@stuff_required
def absecntbarcode(request):

    return render(request, "abscentbarcode.html", {})


@login_required
@stuff_required
def getstbarcode(request):
    code = request.POST.get("code", "0")
    if code =="0":
        HttpResponseRedirect(reverse('manager:absecntparcode') + f"?statue=falsed&&err=entabarcode")
    now1 = datetime.datetime.today()
    H = now1.hour
    M = now1.minute
    now = datetime.time(H, M)

    day = now1.day
    month = now1.month
    year = now1.year
    today = datetime.datetime(year, month, day)
    weekday = dayoftheweek[datetime.datetime.today().weekday()]
    student = Student.objects.filter(barcode=code).first()
    lecture = Lecture.objects.filter(teacher=student.teacher.id, hour__lt=now, day=weekday) \
        .order_by("-hour") \
        .first()
    st=Student_Lecture.objects.filter(lecture=lecture,student=student).first()
    A=Absence(lecture=st, day=today, absence=str(False))
    A.save()
    print(A.id)
    return HttpResponseRedirect(reverse('manager:absecntparcode'))

def changepassword(request):
    return render(request,"changepassword.html",{})






