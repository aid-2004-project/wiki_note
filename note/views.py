from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Note


# Create your views here.


def list_view(request):
    username = request.session["username"]
    uid = request.session["uid"]
    notes = Note.objects.filter(user_id=uid)
    return render(request, "note/list_note.html", locals())


def add_view(request):
    if request.method == "GET":
        return render(request, "note/add_note.html")
    elif request.method == "POST":
        uid = request.session["uid"]
        title = request.POST.get("title")
        content = request.POST.get("content")
        Note.objects.create(title=title, content=content, user_id=uid)
        return HttpResponseRedirect("/note/")


def mod_view(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Exception as e:
        print("---get note error is %s" % e)
        return HttpResponse("This note is not existed")
    if request.method == "GET":
        return render(request, "note/mod_note.html", locals())
    elif request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        note.title = title
        note.content = content
        note.save()
        return HttpResponseRedirect("/note/")


def del_view(request,note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Exception as e:
        print("---get note error is %s" % e)
    note.delete()
    return HttpResponseRedirect("/note/")

