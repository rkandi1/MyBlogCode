from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import UserAccount, BlogPosts
from django.db.models import ObjectDoesNotExist

from hashlib import md5

# todo: Change this during production
from MyBlog.settings import SECRET_KEY


class LoginPage(TemplateView):
    template_name = "admin_accounts/admin-login.html"

    def get(self, request, *args, **kwargs):
        if "userid" in request.COOKIES:
            userid_cookie = request.COOKIES["userid"].split("|")
            if md5((SECRET_KEY+userid_cookie[0]).encode("utf8")).hexdigest() == userid_cookie[1]:
                return HttpResponseRedirect("http://127.0.0.1:8000/admins/mainpage/")

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email_field = request.POST["email"]
        password_field = request.POST["password"]

        error_statement = "Please fill both the user and the password fields."

        if email_field and email_field != "" and password_field and password_field!="":
            curr_user = None
            try:
                curr_user = UserAccount.objects.get(email=email_field)
            except ObjectDoesNotExist:
                error_statement = "There was a problem recording your credentials. Please try again."

            if (curr_user is not None) and (curr_user.password == password_field):
                request.session["email"] = email_field
                # todo: Change url in production
                response = HttpResponseRedirect("http://127.0.0.1:8000/admins/mainpage/")

                cookie_val = "|".join([str(curr_user.id),
                                       md5((SECRET_KEY+str(curr_user.id)).encode("utf8")).hexdigest()])

                response.set_cookie("userid", cookie_val, max_age=1000)
                return response
            else:
                login_error = "The credentials do not exist!"
                return render(request, self.template_name, context={"error": login_error})


        return render(request, self.template_name, context={"error": error_statement,
                                                            "email_val": email_field})


def validate_cookie(get_request):
    if "userid" not in get_request.COOKIES.keys():
        return None

    id_cookie = get_request.COOKIES["userid"].split("|")
    if md5((SECRET_KEY + id_cookie[0]).encode("utf8")).hexdigest() != id_cookie[1]:
        # todo: Maybe change the password hash.
        return None
    else:
        return id_cookie


class AdminMainPage(ListView):
    template_name = "admin_accounts/main_page.html"

    def get(self, request, *args, **kwargs):
        id_cookie = validate_cookie(request)
        if not id_cookie:
            # todo: Change url in production
            return HttpResponseRedirect("http://127.0.0.1:8000/login/")

        posts = BlogPosts.objects.filter(user_id__id=int(id_cookie[0]))
        if len(posts) == 0:
            posts = "There are no posts yet!!"
        request.session["email"] = None
        return render(request, self.template_name, context={"posts":posts})

    def post(self, request, *args, **kwargs):
        print(request.POST["itemtbd"])
        if "itemtbd" in request.POST:
            post = BlogPosts.objects.filter(id=request.POST["itemtbd"])
            print(post)
            for item in post:
                print(item)
                item.delete()

        return HttpResponseRedirect("/admins/mainpage/")


class PostDetail(DetailView):
    template_name = "admin_accounts/post_detail.html"

    def get(self, request, *args, **kwargs):
        id_cookie = validate_cookie(request)
        if not id_cookie:
            return HttpResponseRedirect("http://127.0.0.1:8000/login/")

        posts = BlogPosts.objects.get(id=kwargs.get("postId"))
        title = posts.title
        body = posts.content
        created = posts.created
        return render(request, self.template_name, {"title":title, "body":body,
                                                    "created": created})

    def post(self, request, *args, **kwargs):
        title = request.POST["post-title"]
        body = request.POST["post-content"]
        post_update = BlogPosts.objects.get(id=kwargs.get("postId"))
        post_update.content = body
        post_update.title = title
        post_update.save(update_fields=["title", "content"])
        return HttpResponseRedirect("http://127.0.0.1:8000/admins/mainpage/")
