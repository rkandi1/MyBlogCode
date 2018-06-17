from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from accounts.models import BlogPosts
from django.core.exceptions import ObjectDoesNotExist


class IndexView(TemplateView):
    template_name = "general_view/index.html"

    def get(self, request, *args, **kwargs):
        posts = BlogPosts.objects.all()
        return render(request, self.template_name, {"posts_one":posts[:4], "posts_two":posts[4:8]})


class PostDetailView(DetailView):
    template_name = "general_view/post_detail.html"

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get("postId")
        try:
            posts = BlogPosts.objects.get(id=post_id)
        except ObjectDoesNotExist:
            print("The post does not exist")
            return None

        title = posts.title
        content = posts.content
        created = posts.created.date
        response = render(request, self.template_name, {"title":title, "content":content,
                                                    "created":created})
        response["USER-AGENT"] = "Developer_Name/Rohan_Kandi"
        return response
