from django.urls import path

from teacher import views

app_name = "teacher"

urlpatterns = [
    path("studentlist/",views.showStudent,name="studentlist"),
    path("updatestudentform/<int:id>",views.UpdateStudentForm,name="updatestudentform"),
    path("updatestudent/<int:id>",views.UpdateStudent,name="updatestudent"),
path("addstudentlectureform/<int:id>",views.addstudentlectureform,name="addstudentlectureform"),
path("addstudentlecture/<int:idstudent>/<int:idlecture>",views.addstudentlecture,name="addstudentlectureform"),


path("takeabsence/",views.takeabsence,name="takeabsence"),
path("absence/<int:id>/<str:abs>",views.absence,name="absence"),
path("checkabsence/<int:id>",views.checkabsence,name="checkabsence"),
    ]