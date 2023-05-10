from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views

from .views import list_interviews,home,login_view,register,interview_page,add_interview,add_candidate






urlpatterns = [
    path("interviews/",list_interviews,name='interviews'),
    path('login/',login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/',register,name="register"),
    re_path(r'^interviwes/(?P<interview_id>\d+)/$',interview_page, name='interview_page'),
    path("add-interview/",add_interview,name='add_interview'),
    re_path(r"^add-candidate/(?P<interview_id>\d+)/$",add_candidate,name="add_candidate"),
]