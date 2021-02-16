from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from account.forms import UserSignUpForm
from account.models import Teacher, surat, aya, user, Student
from quranproject.decrorator import stuff_required

listsurat= "البقرة-286,"
print(listsurat)

listsurat+="اّل عمران-200,\
النساء-176,\
المائدة-120,\
الانعام-165,\
الاعراف-206,\
الانفال-75,\
التوبة-129,\
يونس-109,\
هود-123,\
يوسف-111,\
الرعد-43,\
ابراهيم-52,\
الحجر-99,\
النحل-128,\
الاسراء-111,\
الكهف-110,\
مريم-98,\
طه-135,\
الانبياء-112,\
الحج-78,\
المؤمنون-118,\
النور-64,\
الفرقان-77,\
الشعراء-227,\
النمل-93,\
القصص-88,\
العنكبوت-69,\
الروم-60,\
لقمان-34,\
السجدة-30,\
الاحزاب-73,\
سبأ-54,\
فاطر-45,\
يس-83,\
الصافات-182,\
ص-88,\
الزمر-75,\
غافر-85,\
فصلت-54,\
الشوري-53,\
الزخرف-89,\
الدخان-59,\
الجاثية-37,\
الاحقاف-35,\
محمد-38,\
الفتح-29,\
الحجرات-18,\
ق-45,\
الذاريات-60,\
الطور-49,\
النجم-63,\
القمر-55,\
الرحمن-78,\
الواقعة-97,\
الحديد-29,\
المجادلة-22,\
الحشر-24,\
الممتحنة-13,\
الصف-14,\
الجمعة-11,\
المنافقون-11,\
التغابن-18,\
الطلاق-12,\
التحريم-12,\
الملك-30,\
القلم-52,\
الحاقة-52,\
المعارج-44,\
نوح-28,\
الجم-28,\
المزمل-20,\
المدثر-56,\
القيامة-40,\
الانسان-31,\
المرسلات-50,\
النبأ-40,\
النازعات-46,\
عبس-42,\
التكوير-29,\
الانفطار-19,\
المطففين-36,\
الانشقاق-25,\
البروج-22,\
الطارق-17,\
الاعلي-19,\
الغاشية-26,\
الفجر-30,\
البلد-20,\
الشمس-15,\
الليل-21,\
الضحي-11,\
الشرح-8,\
التين-8,\
العلق-19,\
القدر-5,\
البينة-8,\
الفيل-5,\
قريش-4,\
الماعون-7,\
الكوثر-3,\
الكافرون-6,\
النصر-3,\
المسد-5,\
الاخلاص-4,\
الفلق-5,\
الناس-6"



@login_required
def homepage(request):
    user=request.user
    print(type(user.password))
    if user.is_teacher:
        return render(request, "teacher_main_page.html", {})
    if user.is_student:
        return render(request, "student_main_page.html", {})
    if user.is_manager:
        return render(request, "manager_main_page.html", {})
    if user.is_superuser:
        return render(request, "base.html", {})


def login_form(request):
    print(request.GET)
    message=request.GET.get("err","")
    print(message)
    return render(request, "login.html", {
        'msg':message
    })


def login_f(request):

    username = request.POST.get('username')
    password = request.POST.get('password')
    print("name",username)
    print("pass",password)
    user = authenticate(username=username, password=password)
    if user is not None:
        print(user.is_superuser)
        if user.is_active:
            login(request, user)

            return HttpResponseRedirect(reverse('accounts:home'))
        else:
            return HttpResponseRedirect(reverse('accounts:login_form'))



    else:

            return HttpResponseRedirect(reverse('accounts:login_form')+"?err=اسم المستخدم او كلمة السر خطأ")

def logout_f(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:home'))


@login_required
@stuff_required
def changepassword(request):
    password = request.POST.get("password", "0")
    print(password)
    code = request.POST.get("code", "0")
    student=Student.objects.filter(barcode=code).first()
    u=user.objects.filter(id=student.user.id).first()
    user.set_password(u,password)
    u.save()

    return HttpResponseRedirect(reverse('manager:changepassword'))


