from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = [
            "student",
            "amount",
            "payment_date",
            "status",
            "remarks",
        ]

        widgets = {
            "student": forms.HiddenInput(),
            "payment_date": forms.DateInput(attrs={"type": "date"}),
            "remarks": forms.Textarea(attrs={"rows": 3}),
            "amount": forms.NumberInput(attrs={"readonly": "readonly"}),
        }