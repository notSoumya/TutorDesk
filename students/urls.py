from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("students/", views.student_list, name="student_list"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/<int:pk>/",views.student_detail,name="student_detail"),
    path("students/edit/<int:pk>/",views.edit_student,name="edit_student"),
    path("students/delete/<int:pk>/",views.delete_student,name="delete_student"),
]