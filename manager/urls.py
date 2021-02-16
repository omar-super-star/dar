from django.urls import path

from manager import views

app_name = "manager"

urlpatterns = [
    path("addteacherform/",views.addTeacherForm,name="addteacherform"),
path("addteacher/",views.addTeacher,name="addteacher"),
    path("teacherlist/",views.showTeacher,name="teacherlist"),
path("teacherdetail/<int:id>",views.teacherdetail,name="teacherdetail"),



 path("addstudentform/",views.addStudentForm,name="addstudentform"),
path("addstudent/",views.addStudent,name="addstudent"),
path("updatestudent/<int:pk>",views.StudentUpdateView.as_view(),name="updatestudent"),
    path("studentlist/",views.showStudent,name="studentlist"),
path("studentdetail/<int:id>",views.studentdetail,name="studentdetail"),
path("paidstudent/<int:id>",views.paidstudent,name="paid"),
path("studentlistteacher/<int:id>",views.showStudentTeacher,name="studentlistteacher"),


path("addlectureform/",views.addLecturetForm,name="addlectureform"),
path("addlecture/",views.addLecture,name="addlecture"),
    path("lecturelist/",views.showLecture,name="lecturelist"),
path("lecturedetail/<int:id>",views.lecturedetail,name="lecturedetail"),
path("studentlecturelist/<int:id>",views.showStudentLecture,name="studentlecturelist"),
path("lecturelisttecaher/<int:id>",views.showLectureTeacher,name="lecturelistteacher"),

path("abscentbyparcode/",views.absecntbarcode,name="absecntparcode"),
path("readparcode/",views.getstbarcode,name="readparcode"),

path("changepassword/",views.changepassword,name="changepassword"),

    ]