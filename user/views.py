from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from user.models import User
from note.models import Note
import hashlib
from functools import wraps


# from django.

# Create your views here.

def judge_login(func):
    @wraps(func)
    def wrapper(request):
        if request.method == "GET":
            # 如果用户已登录 显示 已登录
            # 优先检查session
            rlt = False
            if "username" in request.session and \
                    "uid" in request.session:
                rlt = True
                # 检查Cookies
            else:
                username = request.COOKIES.get("username")
                uid = request.COOKIES.get("uid")
                if username and uid:
                    request.session["username"] = username
                    request.session["uid"] = uid
                    rlt = True
            return func(request,rlt)
        else:
            return func(request)
    return wrapper

@judge_login
def log_view(request,rlt=False):
    if request.method == "GET":
        if rlt:
            # username = request.session["username"]
            # return render(request,"index/index.html",locals())
            return HttpResponseRedirect("/index")
        return render(request, "user/login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        # 利用唯一索引判断用户是否存在
        try:
            old_user = User.objects.get(username=username)
        except Exception as e:
            print("--login get error %s" % e)
            return HttpResponse("用户名或密码错误")

        m = hashlib.md5()
        m.update(password.encode())
        password_h = m.hexdigest()
        # user = User.objects.filter(username=username, password=password_h)
        if old_user.password != password_h:
            return HttpResponse("用户名或密码错误")
        # 存储回话状态
        request.session["uid"] = old_user.id
        request.session["username"] = username

        # 判断是否要存储Cookies
        # resp = HttpResponse("登录成功！")
        resp = HttpResponseRedirect("/index")
        # resp = render(request, "index/index.html", {"username": username})
        if "rem_name" in request.POST:
            resp.set_cookie("username", username, 3 * 24 * 3600)
            resp.set_cookie("uid", old_user.id, 3 * 24 * 3600)
        return resp


def reg_view(request):
    if request.method == "GET":
        return render(request, "user/register.html")
        # return HttpResponse("注册页面")
    elif request.method == "POST":
        username = request.POST.get("username")
        user = User.objects.filter(username=username)
        if user:
            return HttpResponse("用户名已存在")
        password = request.POST.get("pwd")
        pwd_again = request.POST.get("pwd_again")
        if password != pwd_again:
            return HttpResponse("两次输入的密码不一致")
        # 处理密码 - hash算法【散列】
        # 算法特点
        # 1,不可逆
        # 2.输入不变 输出不变
        # 3.定长输出 【明文不同，算法恒定，则输出长度一定】
        # 4，雪崩 - 文件完整性校验 -BAT -40G 下载完后如何计算hash值
        m = hashlib.md5()
        m.update(password.encode())
        password_h = m.hexdigest()
        try:
            user = User.objects.create(username=username, password=password_h)
        except Exception as e:
            print("--create error is %s" % e)
            return HttpResponse("用户名已存在")
        # 免登陆一天
        request.session["uid"] = user.id
        request.session["username"] = user.username
        return HttpResponse("注册成功")


def logout_view(request):
    resp = HttpResponseRedirect("/index")
    resp.delete_cookie("username")
    resp.delete_cookie("uid")
    request.session.clear()
    return resp

@judge_login
def note_in(request,rlt = False):
    if rlt==True:
        return HttpResponseRedirect("/note/")
    else:
        return HttpResponseRedirect("login")
