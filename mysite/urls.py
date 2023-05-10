"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include,re_path
from core.views import test_view,list_interviews,home,login_view,register,interview_page,add_interview,add_candidate
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("interviews/",list_interviews,name='interviews'),
    # path('login/',login_view, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    # path('register/',register,name="register"),
    # re_path(r'^interviwes/(?P<interview_id>\d+)/$',interview_page, name='interview_page'),
    # path("add-interview/",add_interview,name='add_interview'),
    # re_path(r"^add-candidate/(?P<interview_id>\d+)/$",add_candidate,name="add_candidate"),
    path("",include('core.urls'))
]
