from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth

from .models import Student
from .forms import StudentForm
from payments.models import Payment

@login_required
def home(request):

    total_students = Student.objects.count()

    recent_students = Student.objects.order_by("-created_at")[:5]

    today = date.today()

    # Current Month Revenue
    monthly_revenue = (
        Payment.objects.filter(
            status="Paid",
            payment_date__month=today.month,
            payment_date__year=today.year,
        ).aggregate(total=Sum("amount"))["total"] or 0
    )

    # Pending Fees
    pending_fees = 0

    for student in Student.objects.filter(is_active=True):

        paid = Payment.objects.filter(
            student=student,
            payment_date__month=today.month,
            payment_date__year=today.year,
            status="Paid",
        ).exists()

        if not paid:
            pending_fees += student.monthly_fee

    # Due Today
    due_today = Student.objects.filter(
        due_day=today.day,
        is_active=True
    ).count()

    # Revenue Chart
    monthly_data = (
        Payment.objects.filter(status="Paid")
        .annotate(chart_month=TruncMonth("payment_date"))
        .values("chart_month")
        .annotate(total=Sum("amount"))
        .order_by("chart_month")
    )

    chart_labels = []
    chart_values = []

    for item in monthly_data:
        chart_labels.append(item["chart_month"].strftime("%b %Y"))
        chart_values.append(float(item["total"]))

    context = {
        "total_students": total_students,
        "recent_students": recent_students,
        "monthly_revenue": monthly_revenue,
        "pending_fees": pending_fees,
        "due_today": due_today,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
    }

    return render(request, "students/dashboard.html", context)

@login_required
def student_list(request):

    query = request.GET.get("q", "")

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(name__icontains=query)
            | Q(phone__icontains=query)
            | Q(parent_name__icontains=query)
        )

    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
            "query": query,
        },
    )

@login_required
def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "students/add_student.html",
        {
            "form": form,
        },
    )

@login_required
def edit_student(request, pk):

    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":

        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "students/edit_student.html",
        {
            "form": form,
            "student": student,
        },
    )

@login_required
def student_detail(request, pk):

    student = get_object_or_404(Student, id=pk)

    payments = Payment.objects.filter(
        student=student
    ).order_by("-payment_date")

    context = {
        "student": student,
        "payments": payments,
    }

    return render(
        request,
        "students/student_detail.html",
        context,
    )

from django.contrib import messages

@login_required
def delete_student(request, pk):

    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")

    return render(
        request,
        "students/delete_student.html",
        {
            "student": student,
        },
    )