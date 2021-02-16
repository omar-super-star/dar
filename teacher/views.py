import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from account.models import Student, aya, Lecture, Student_Lecture, Absence, surat, Degree
from manager.forms import HomeWorkDegree, StudentFormmanager, StudentFormSuperUser
from quranproject.decrorator import teacher_required, stuff_required, not_student_required

absdict={"true":True,
         "false":False}
dayoftheweek=["الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]


@login_required
@teacher_required
def showStudent(request):
    num = request.GET.get("page", 1)
    objects =Student.objects.filter(teacher=request.user.teacher.id).all()
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
@not_student_required
def UpdateStudentForm(request, id):
    user = request.user
    print(request.POST)
    student = Student.objects.filter(id=id).first()
    if user.is_manager:
        return render(request, "updatestudentm.html", {
            "student":student,
           "form_student":StudentFormmanager(user1=user,initial={
               "teacher":student.teacher,
               "name":student.name,
               "fathername":student.fathername,
               "fathernumber":student.fathernumber,
               "gender":student.gender,
               "notpaid":student.notpaid,
               "resoenofnotpaid":student.resoenofnotpaid,
               "paymount":student.paymount,
               "degree":student.degree,
           })
        })
    elif user.is_superuser:
        return render(request, "updatestudentm.html", {
            "student": student,
            "form_student": StudentFormmanager( initial={
                "teacher": student.teacher,
                "name": student.name,
                "fathername": student.fathername,
                "fathernumber": student.fathernumber,
                "gender": student.gender,
                "notpaid": student.notpaid,
                "resoenofnotpaid": student.resoenofnotpaid,
                "paymount": student.paymount,
                "degree": student.degree,
            })
        })

    homework=request.GET.get("homework","false")
    homework=absdict[homework]
    ida = int(request.GET.get("ida", 0))



    return render(request,"updatestudent.html",{
        "student":student,
        "homework":homework,
        "degree": HomeWorkDegree,
        "ida":ida
    })


@login_required
@stuff_required
def UpdateStudent(request,id):
    user=request.user
    print(request.POST)
    student = Student.objects.filter(id=id).first()
    newaya = request.POST.get("aya")
    degree=request.POST.get("degree")
    homework=request.POST.get("homework")
    homeworkdegree=request.POST.get("homeworkdegree",None)
    ida=int(request.POST.get("ida",0))
    degree=Degree.objects.filter(name=degree).first()
    if degree==None:
        degree=student.degree.id
    else:
        degree=degree.id
    if newaya == "":
        newaya=f'{student.aya.numberinsurat}:{student.aya.surat.numberinquran}'
    if homework == "":
        homework=f'{student.homework}'
    if len(newaya.split(":"))!= 2:
        return HttpResponseRedirect(reverse('manager:studentdetail', kwargs={'id': id})+f"?err=ادخل رقم اية في صورة صحيحة ")
    numberofnewaya=newaya.split(":")[0]
    numberofsuratofaya=newaya.split(":")[1]
    if not numberofsuratofaya.isnumeric():
        s=surat.objects.filter(name=numberofsuratofaya).first()
        if s==None:
            return HttpResponseRedirect(
                reverse('manager:studentdetail', kwargs={'id': id}) + f"?err=ادخل رقم اية في صورة صحيحة ")
        else:
            numberofsuratofaya=s.id
    a=aya.objects.filter(numberinsurat=int(numberofnewaya),surat__numberinquran=int(numberofsuratofaya)).first()
    if a== None:
        return HttpResponseRedirect(
            reverse('manager:studentdetail', kwargs={'id': id}) + f"?err=ادخل رقم اية في صورة صحيحة ")
    student.aya=a
    student.degree=degree
    student.homework=homework
    student.save()

    if homework:
        A = Absence.objects.filter(id=ida).first()
        A.homeworkdegree = homeworkdegree
        A.save()
        return HttpResponseRedirect(reverse('teacher:takeabsence')+f"hwseen={id}_{A.id}")
    return HttpResponseRedirect(reverse('manager:studentdetail',kwargs={'id': id}))

@login_required
@teacher_required
def addstudentlectureform(request,id):
    num = request.GET.get("page", 1)
    lecture=Lecture.objects.filter(id=id).first()
    objects = Student.objects.filter(teacher=lecture.teacher.id)\
        .exclude(student_lecture__in=Student_Lecture.objects.filter(lecture__id=id))\
        .all()
    print(objects)
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
    context["lecture"]=lecture

    return render(request, "studentlecture.html", context)


@login_required
@teacher_required
def addstudentlecture(request,idstudent,idlecture):
    student=Student.objects.filter(id=idstudent).first()
    lecture = Lecture.objects.filter(id=idlecture).first()
    Student_Lecture(student=student,lecture=lecture).save()
    return JsonResponse({"id":idstudent})




@login_required
@teacher_required
def takeabsence(request):
    num = request.GET.get("page", 1)
    now1=datetime.datetime.now()
    H=now1.hour
    M=now1.minute
    now=datetime.time(H,M)
    weekday=dayoftheweek[datetime.datetime.today().weekday()]
    print(datetime.datetime.today())
    print(datetime.datetime.today().weekday())
    print(weekday)
    print("here error")
    lecture=Lecture.objects.filter(teacher=request.user.teacher.id,hour__lt=now,day=weekday)\
        .order_by("-hour")\
        .first()
    print(lecture)
    objects = Student_Lecture.objects.filter(lecture=lecture).all()
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
    context["lecture"] = lecture


    return render(request, "takeabsence.html", context)
@login_required
@teacher_required
def absence(request,id,abs):
    student=Student_Lecture.objects.filter(id=int(id)).first()
    print(student)
    idstudent=student.student.id
    now=datetime.datetime.now()
    day=now.day
    month=now.month
    year=now.year
    today=datetime.datetime(year,month,day)
    A=Absence.objects.filter(lecture=student,day=today).first()
    if  A== None:
        A=Absence(lecture=student,day=today,absence=str(absdict[abs]))
        A.save()
    else:
        A.absence=absdict[abs]
        A.save()
    id=A.id
    return JsonResponse({"id":str(idstudent)+"_"+str(absdict[abs]),
                         "idc":str(idstudent)+"_"+ str(not absdict[abs]),
                         "ida":str(id)})
@login_required
@teacher_required
def checkabsence(request,id):
    num=request.GET.get("page", 1)
    lecture=Lecture.objects.filter(id=int(id)).first()
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    year = now.year
    today = datetime.datetime(year, month, day)
    Abs=Absence.objects.filter(lecture__lecture=lecture,day=today).all()
    pages = Paginator(Abs, 50)
    Abs = pages.page(num)
    context=[]
    for i in Abs.object_list:
        ids=i.lecture.student.id
        statue=i.absence
        id = i.id
        context.append({
            "id": str(ids) + "_" + str(statue),
            "idc": str(ids) + "_" + str(not statue),
            "ida": str(id),
            "degree":i.homeworkdegree,
        })
    return JsonResponse({"res":context})

#
