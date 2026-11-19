from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("submit/", views.submit_complaint, name="submit"),
    path("status/<int:pk>/<str:status>/", views.change_status, name="status"),
    path("delete/<int:pk>/", views.delete_complaint, name="delete"),
]