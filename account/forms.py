from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from account.models import user


class UserSignUpForm(UserCreationForm):
    class Meta():
        model = user
        fields = ("username", "password1", "password2",)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "اسم المستخدم هذا الاسم يجب مختلفا عن باقي الاسماء يستخدمه في تسجيل الدخول "
        self.fields["password1"].label = "كلمة السر"
        self.fields["password2"].label = "تأكيد كلمة السر"

        for  field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None

class UserUpdateForm(UserCreationForm):
    class Meta():
        model = user
        fields = ("username", "email", 'first_name', 'last_name',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "اسم المستخدم"
        self.fields["email"].label = "البريد الالكترونى"
        self.fields["first_name"].label = "الاسم الاول "
        self.fields["last_name"].label = "الاسم الاخير"


        for  field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None

class UserChangePasswordForm(UserCreationForm):
    class Meta():
        model = user
        fields = ( "password1", "password2",)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "كلمة السر"
        self.fields["password2"].label = "تأكيد كلمة السر"

        for  field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None