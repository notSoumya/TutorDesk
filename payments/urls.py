from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:student_id>/", views.add_payment, name="add_payment"),
    path("add/<int:student_id>/", views.add_payment, name="collect_fee"),
    path("", views.payment_list, name="payment_list"),
]