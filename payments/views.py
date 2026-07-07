from django.shortcuts import render, redirect
from .forms import PaymentForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from students.models import Student
from .forms import PaymentForm
from .models import Payment

@login_required
def payment_list(request):
    payments = Payment.objects.select_related("student").order_by("-payment_date")

    return render(
        request,
        "payments/payment_list.html",
        {
            "payments": payments,
        },
    )

@login_required
def add_payment(request, student_id):

    if student_id:
        student = get_object_or_404(Student, id=student_id)
    else:
        student = None

    if request.method == "POST":

        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)

    # Automatically derive month from payment_date
            payment.month = payment.payment_date.strftime("%B %Y")

            payment.save()

            return redirect("payment_list")

    else:

        if student:
            form = PaymentForm(initial={
            "student": student,
            "amount": student.monthly_fee,
            "month": date.today().strftime("%B %Y"),
            "payment_date": date.today(),
            "status": "Paid",
        })
        else:
            form = PaymentForm()

    return render(
    request,
    "payments/add_payment.html",
    {
        "form": form,
        "student": student,
    }
)