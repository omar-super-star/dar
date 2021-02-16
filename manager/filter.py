import django_filters
from django import forms

from account.models import Student, Teacher, Manager


class StudentFilter(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = ['name',
                  "teacher__id",
                  "degree__name",
                  "teacher__manager",
                  "gender",
                  ]



class StudentFilterFormManager(forms.ModelForm):
    name=forms.CharField()
    teacher__id = forms.ModelChoiceField(queryset=Teacher.objects.all())
    degree__name = forms.CharField()

    class Meta:
        model = Student
        fields = ('name',
                  "teacher__id",
                  "degree__name",
                  "gender",
                  )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user1', None)
        super().__init__(*args, **kwargs)

        self.fields["name"].label="اسم الطالب"
        self.fields["degree__name"].label = "المرحلة"
        self.fields["teacher__id"].label = "المدرس"
        self.fields["gender"].label = "الجنس"
        self.fields["name"].required=False
        self.fields["teacher__id"].required=False
        self.fields["degree__name"].required = False
        self.fields["gender"].required = False
        self.fields["teacher__id"].queryset=Teacher.objects.filter(manager=user.manager.id)



class StudentFilterFormSuperUser(forms.ModelForm):
    name = forms.CharField()
    teacher__id = forms.ModelChoiceField(queryset=Teacher.objects.all())
    teacher__manager = forms.ModelChoiceField(queryset=Manager.objects.all())
    degree__name = forms.CharField()
    class Meta:
        model = Student
        fields = ('name',
                  "teacher__id",
                  "degree__name",
                  "teacher__manager",
                  "gender",
                  )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user1', None)
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "اسم الطالب"
        self.fields["gender"].label = "الجنس"
        self.fields["degree__name"].label = "المرحلة"
        self.fields["teacher__id"].label = "المدرس"
        self.fields["teacher__manager"].label = "الفرع"
        self.fields["name"].required = False
        self.fields["teacher__id"].required = False
        self.fields["degree__name"].required = False
        self.fields["teacher__manager"].required = False
        self.fields["gender"].required = False
        #self.fields["group"].queryset=Group.objects.filter(teacher=teacher)



class StudentFilterFormTeacher(forms.ModelForm):
    name = forms.CharField()

    degree__name = forms.CharField()
    class Meta:
        model = Student
        fields = ('name',
                 "degree__name",
                  "gender",
                 )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user1', None)
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "اسم الطالب"
        self.fields["degree__name"].label = "المرحلة"
        self.fields["gender"].label = "الجنس"
        self.fields["name"].required = False
        self.fields["gender"].required = False
        self.fields["degree__name"].required = False

