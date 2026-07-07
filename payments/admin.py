from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "amount",
        "payment_date",
        "status",
    )

    list_filter = (
        "status",
        "payment_date",
    )

    search_fields = (
        "student__name",
    )