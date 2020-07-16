from index import views
from django.urls import path

urlpatterns = [
    path("index",views.index_view),
    # path("index",views.index_login),
]