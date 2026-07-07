from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            "name",
            "parent_name",
            "phone",
            "student_class",
            "school",
            "monthly_fee",
            "joining_date",
            "due_day",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "parent_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "student_class": forms.TextInput(attrs={"class": "form-control"}),
            "school": forms.TextInput(attrs={"class": "form-control"}),
            "monthly_fee": forms.NumberInput(attrs={"class": "form-control"}),
            "joining_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "due_day": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }