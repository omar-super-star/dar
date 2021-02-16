import os
import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
# Create your models here.
from account.barcodegenrator import MyBarcodeDrawing
gender_choices = (('Male',"Male"),
                ('Female',"Female"),)
day_choices=(
    ("السبت","السبت"),
    ("الأحد","الأحد"),
    ("الاثنين","الاثنين"),
    ("الثلاثاء","الثلاثاء"),
    ("الاربعاء","الاربعاء"),
    ("الخميس","الخميس"),
    ("الجمعة","الجمعة"),

)

absence_choices=(("parcode","parcode"),
                 ("teacher","teacher"),
)

homeworkdegreechoices=(("ممتاز","ممتاز"),
                       ("جيد جدا","جيد جدا"),
                       ("جيد","جيد"),
                       ("مقبول","مقبول"),
                       ("اعادة","اعادة"))


class user(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_manager   = models.BooleanField(default=False)
    def save(self,*args,**kwargs):
        if "pbkdf2_sha256" != self.password.split("$")[0]:
            self.set_password(self.password)
        return super().save()


class surat(models.Model):
    name=models.CharField(max_length=255,null=False)
    numberinquran=models.PositiveIntegerField()
    numberofayat=models.PositiveIntegerField(null=True,blank=True)
    def __str__(self):
        return f"{self.name}"


class juz(models.Model):
    name=models.CharField(max_length=255,null=False)
    numberinquran = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.name}"


class hizp(models.Model):
    name = models.CharField(max_length=255, null=False)
    numberinquran = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.name}"


class ruba(models.Model):
    name = models.CharField(max_length=255, null=False)
    numberinquran = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.name}"


class aya(models.Model):
    surat=models.ForeignKey(surat, on_delete=models.CASCADE, related_name='surat')
    juz=models.ForeignKey(juz, on_delete=models.CASCADE, related_name='juz',null=True)
    hizp=models.ForeignKey(hizp, on_delete=models.CASCADE, related_name='hizp',null=True)
    ruba=models.ForeignKey(ruba, on_delete=models.CASCADE, related_name='ruba',null=True)
    numberinsurat= models.PositiveIntegerField()
    numberinquran=models.PositiveIntegerField()
    def __str__(self):
        return f"{self.surat}:{self.numberinsurat}"


class Manager(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='manager')

    def __str__(self):
        return f"{self.user.username}"


class Teacher(models.Model):
    user=models.OneToOneField(user, on_delete=models.CASCADE, related_name='teacher')
    manager=models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='manager_teacher',null=True,blank=True)
    def __str__(self):
        return f"{self.user.username}"


class Lecture(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lecture_teacher',null=True,blank=True)
    day=models.CharField(max_length=20,choices=day_choices)
    types = models.CharField(max_length=30,null=True,blank=True)
    hour=models.TimeField(null=True,blank=True)
    def __str__(self):
        return f"{self.teacher.user.username}-{self.day}-{self.hour}"

class Degree(models.Model):
    name=models.CharField(max_length=15,null=True,blank=True)
    def __str__(self):
        return f"{self.name}"

class Student(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='student',null=True,blank=True)
    name=models.CharField(max_length=25, null=True,blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='student_teacher',null=True,blank=True)
    aya = models.ForeignKey(aya, on_delete=models.CASCADE, related_name='student_aya', null=True,blank=True)
    Achievements = models.CharField(max_length=2500, null=True,blank=True)
    barcode = models.CharField(max_length=2500, null=True,blank=True)
    degree=models.ForeignKey(Degree, on_delete=models.CASCADE, related_name='student_degree', null=True,blank=True)
    fathername = models.CharField(max_length=15, null=True, blank=True)
    fathernumber=models.CharField(max_length=20, null=True, blank=True)
    homework=models.CharField(max_length=2500, null=True,blank=True)
    gender=models.CharField(max_length=10,choices=gender_choices, null=True,blank=True)
    notpaid=models.BooleanField(null=True,blank=True)
    resoenofnotpaid=models.CharField(max_length=2500, null=True,blank=True)
    paid=models.BooleanField(null=True,blank=True)
    paymount=models.FloatField(null=True,blank=True)
    birthday=models.DateTimeField(null=True,blank=True)
    startlogin=models.DateTimeField(null=True,blank=True)
    finishlogin=models.DateTimeField(null=True,blank=True)

    def paidf(self):
        ds = datetime.now()
        df = ds + timedelta(30)
        self.startlogin = ds
        self.finishlogin = df
        self.paid=True
        self.save()
    def __str__(self):
        return f"{self.name}"
    def delete(self):
        os.remove(f"./static/barcodes/{self.user.username}.jpg")
        return super().delete()


class Student_Lecture(models.Model):
    lecture= models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='lecture_student')
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_lecture')


class Absence(models.Model):
    lecture = models.ForeignKey(Student_Lecture, on_delete=models.CASCADE, related_name='lecture_absence')
    day=models.DateTimeField(default=datetime.now())
    absence=models.BooleanField()
    homeworkdegree = models.CharField(max_length=20, choices=homeworkdegreechoices,null=True,blank=True)


class Settings(models.Model):
    manager=models.OneToOneField(Manager, on_delete=models.CASCADE, related_name='manager_settings',null=True,blank=True)
    absence=models.CharField(max_length=25,choices=absence_choices,default='parcode')



