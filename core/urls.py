from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views

from .views import list_interviews,add_interview
from .profile_views import login_view,register
from .interview_status_view import interview_page,add_candidate
from .access_control_views import add_access_control,remove_access




urlpatterns = [
    path("interviews/",list_interviews,name='interviews'),
    path('login/',login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/',register,name="register"),
    re_path(r'^interviews/(?P<interview_id>\d+)/$',interview_page, name='interview_page'),
    path("add-interview/",add_interview,name='add_interview'),
    re_path(r"^add-candidate/(?P<interview_id>\d+)/$",add_candidate,name="add_candidate"),
    re_path(r"^access-control/(?P<interview_id>\d+)/$",add_access_control,name="show_access_control"),
    re_path(r"^remove_access-control/(?P<userinterview_id>\d+)/$",remove_access,name="remove_access"),
    
]