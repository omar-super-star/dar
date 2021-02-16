from django import forms

from account.models import Teacher, Student, Lecture, Absence


class StudentFormmanager(forms.ModelForm):

    degree=forms.CharField()
    class Meta():
        model = Student
        exclude = ("user","aya",
                   "barcode","startlogin","finishlogin",
                   "Achievements","homework",
                   "paid","degree","birthday")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user1', None)
        super().__init__(*args, **kwargs)
        self.fields["teacher"].label="المدرس"
        self.fields["name"].label = "الاسم هذا الاسم الذي سيظهر للمدرس"
        self.fields["fathername"].label = "اسم ولي الامر"
        self.fields["fathernumber"].label = "رقم ولي الامر"
        self.fields["gender"].label = "الجنس"
        self.fields["notpaid"].label = "معفي من الدفع"
        self.fields["resoenofnotpaid"].label = "سبب الاعفاء"
        self.fields["paymount"].label = "قيمة الدفع اذا لم يكن معفيا"
        self.fields["degree"].label = "المستوى"
        self.fields["degree"].required = False
        if user != None:
            self.fields["teacher"].queryset=Teacher.objects.filter(manager=user.manager).all()
        for  field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None



class StudentFormSuperUser(forms.ModelForm):
    degree = forms.CharField()
    class Meta():
        model = Student
        exclude = ("user", "aya",
                   "barcode", "startlogin", "finishlogin",
                   "Achievements", "homework",
                   "paid", "degree", "birthday")

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields["teacher"].label = "المدرس"
        self.fields["name"].label = "الاسم هذا الاسم الذي سيظهر للمدرس"
        self.fields["fathername"].label = "اسم ولي الامر"
        self.fields["fathernumber"].label = "رقم ولي الامر"
        self.fields["gender"].label = "الجنس"
        self.fields["notpaid"].label = "معفي من الدفع"
        self.fields["resoenofnotpaid"].label = "سبب الاعفاء"
        self.fields["paymount"].label = "قيمة الدفع اذا لم يكن معفيا"
        self.fields["degree"].label = "المستوى"
        self.fields["degree"].required = False
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None


class LectureCreateForm(forms.ModelForm):

    class Meta():
        model = Lecture
        exclude=("hour","teacher",)
        fields='__all__'

class LectureCreateTeacherForm(forms.ModelForm):

    class Meta():
        model = Lecture
        fields=("teacher",)

    def __init__(self, *args, **kwargs):
        teachers = kwargs.pop('teachers')

        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = teachers
        for  field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None

class HomeWorkDegree(forms.ModelForm):

    class Meta():
        model = Absence
        fields=("homeworkdegree",)