from django.shortcuts import render


# Create your views here.
def index_view(request):
    username = request.session.get("username","")
    return render(request, "index/index.html",locals())

#
# def index_login(request):
#     username = request.session["username"]
#     return render(request, "index/index.html", locals())
