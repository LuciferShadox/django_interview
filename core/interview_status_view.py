from django.shortcuts import render,redirect
from core.models import Interview,Candidate,UserInterview,User
from django.contrib.auth.decorators import login_required
from django.contrib import messages #import messages

import logging

logger = logging.getLogger(__name__)

@login_required
def add_candidate(request,interview_id):
    if request.method=='POST':
        logger.info("Request is Post")
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        nationality = request.POST["nationality"]
        passport_no = request.POST["passport_no"]
        try:
            visa_issued = bool(request.POST["visa_issued"])
        except:
            visa_issued=False
        try:
            medical_issued = bool(request.POST["medical_issued"])
        except:
            medical_issued = False
        
        cv_file_path = request.POST["file"]
        logger.info("Form Arguments are processed")
        created_by = request.user.username
        candidate = Candidate(first_name=first_name,last_name=last_name,
                              nationality=nationality,passport_no=passport_no,
                              visa_issued=visa_issued,medical_issued=medical_issued,
                              cv_file_path=cv_file_path,created_by=created_by)
        candidate.save()
        interview = Interview.objects.get(id=interview_id)
        interview.candidates.add(candidate)
        interview.save()
        logger.info("Candidate Added")
        return redirect("interview_page",interview_id)
    context ={
        "interview_id": interview_id
    }
    return render(request,"add_candidate.html",context)


@login_required
def interview_page(request,interview_id):
    interview = Interview.objects.get(id=interview_id)
    #TODO have to filter candidates based on creator 
    candidates = interview.get_candidates()
    # user_interview = UserInterview.objects.get(user=request.user,interview=interview_id)
    context={
        "candidates":candidates,
        "access": request.user.access_control,
        "interview_id": interview_id
    }

    return render(request,"interview_status.html",context=context)
# 