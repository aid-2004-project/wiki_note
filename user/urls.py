from django.urls import path
from . import views

urlpatterns = [
    path("reg", views.reg_view),
    path("login", views.log_view),
    path("logout",views.logout_view),
    path("note_in",views.note_in),
]
