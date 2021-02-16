from django.urls import path

from student import views

app_name = "student"

urlpatterns = [
    path("studentabscent/",views.gettheabscent,name="studenabscent"),
    path("studentabscentdata/<int:id>",views.gettheabscentdata,name="studenabscentdata"),
    ]