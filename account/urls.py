from django.urls import path

from account import views

app_name = "accounts"

urlpatterns = [
    path("",views.homepage,name="home"),
    path("login_form/",views.login_form,name="login_form"),
    path("login/",views.login_f,name="login"),
   path("logout/",views.logout_f,name="logout"),
path("changepassword/",views.changepassword,name="changepassowrd"),

    ]