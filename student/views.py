from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from account.models import *
from quranproject.decrorator import student_required


@login_required
@student_required
def gettheabscent(request):
    num = request.GET.get("page", 1)
    objects = Absence.objects.filter(lecture__student__id=request.user.student.id,absence=True).all()
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
    context["student"]=request.user.student
    context['students'] = students
    context["pages"] = pages.page_range
    context["total"]=Absence.objects.filter(lecture__student__id=request.user.student.id).all().count()-objects.count()
    context["absence"] = True
    return render(request,"studentabsence.html",context)

@login_required
def gettheabscentdata(request,id):
    num = int(request.GET.get("page", 1))
    id=int(id)
    objects = Absence.objects.filter(lecture__student__id=id).all()
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
    context["student"] = Student.objects.filter(id=id).first()
    context['students'] = students
    context["pages"] = pages.page_range
    context["total"]=objects.count()-Absence.objects.filter(lecture__student__id=id,absence=str(True)).all().count()


    return render(request,"studentabsence.html",context)