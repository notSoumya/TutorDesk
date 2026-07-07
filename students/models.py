from django.db import models


class Student(models.Model):

    name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    student_class = models.CharField(max_length=20)
    school = models.CharField(max_length=100)

    monthly_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    joining_date = models.DateField()

    due_day = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name