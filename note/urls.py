from django.urls import path,re_path
from . import views


urlpatterns =[
    path("",views.list_view),
    path("add/",views.add_view),
    re_path("mod/(\d+)",views.mod_view),
    re_path("del/(\d+)",views.del_view),
]

