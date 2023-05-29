from django.shortcuts import render,redirect
from core.models import Interview,Candidate,UserInterview,User
from django.contrib.auth.decorators import login_required
from django.contrib import messages #import messages

import logging

logger = logging.getLogger(__name__)


@login_required
def add_access_control(request,interview_id):
    if request.user.is_staff:
        if request.method=='POST':
            user_id = request.POST["user_id"]
            user = User.objects.get(id=user_id)
            interview = Interview.objects.get(id=interview_id)
            if UserInterview.objects.filter(user = user,interview=interview).exists():
                messages.warning(request,"User Already exists")
            else:
                interview_users = UserInterview(user = user,interview=interview)
                interview_users.save()
                messages.info(request,"Access has been updated.")
        
        users_accessing_interview = UserInterview.objects.filter(interview=interview_id)
        users = User.objects.exclude(id=request.user.id)
        print(users)
        context={
            "users":users,
            "interview_users" :users_accessing_interview,
            "interview_id" :interview_id

        }
        return render(request,'access_control.html',context=context)
            
    messages.warning(request,"You Dont Have Permission For this")
    return redirect("interviews")


@login_required
def remove_access(request,userinterview_id):
    user_interview_instance = UserInterview.objects.get(id=userinterview_id)
    interview_id = user_interview_instance.interview.id
    if request.user.is_staff:
        if request.user.id == user_interview_instance.user.id:
            messages.warning(request,"Cannot Delete your self")
            return redirect('show_access_control',interview_id)
        else:
            
            user_interview_instance.delete()
            messages.info(request,"User has been deleted")
            return redirect('show_access_control',interview_id)
        
    return redirect("interview_page",interview_id)

