"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import LoginPage, AdminMainPage, PostDetail
from general_view.views import IndexView, PostDetailView

urlpatterns = [
    # accounts
    path('admin/', admin.site.urls),
    path('login/', LoginPage.as_view(), name="login_page"),
    path('admins/mainpage/', AdminMainPage.as_view(), name="admin_mainpage"),
    path('admins/mainpage/<int:postId>', PostDetail.as_view(), name="post_detail"),

    # viewer page
    path('', IndexView.as_view(), name="index_page"),
    path('<int:postId>/', PostDetailView.as_view(), name="post_detail_view")
]
