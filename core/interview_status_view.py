from django.shortcuts import render,redirect
from core.models import Interview,Candidate,Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages #import messages
from django.core.files import File
from core.utils import notify_all_company_and_client_users
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
        category_name = request.POST["category"]
        try:
            visa_issued = bool(request.POST["visa_issued"])
        except:
            visa_issued=False
        try:
            medical_issued = bool(request.POST["medical_issued"])
        except:
            medical_issued = False
        cv_file_path = request.FILES["file"]
        logger.info("Form Arguments are processed")
        created_by = request.user.username
        candidate = Candidate(first_name=first_name,last_name=last_name,
                              nationality=nationality,passport_no=passport_no,
                              visa_issued=visa_issued, medical_issued=medical_issued,\
                               cv_file_path=cv_file_path,created_by=created_by)
        try:
            category = Category.objects.get(name = category_name)
        except:
            category = Category(name=category_name)
            category.save()
        candidate.category = category
        candidate.save()
        interview = Interview.objects.get(id=interview_id)
        interview.candidates.add(candidate)
        interview.save()
        logger.info("Candidate Added")
        message_to_send= f"{first_name} {last_name} added ."
        notify_all_company_and_client_users(request.user,message_to_send,interview_id)
        return redirect("interview_page",interview_id)
    context ={
        "interview_id": interview_id,
        "categories": Category.objects.all()
    }
    return render(request,"add_candidate.html",context)


@login_required
def interview_page(request,interview_id):
    interview = Interview.objects.get(id=interview_id)

    if request.user.access_control == "CO" or  request.user.access_control == "CL" :
        candidates = interview.get_candidates()
    else:
        candidates = interview.candidates.filter(created_by=request.user.username)
    
    context={
        "candidates":candidates,
        "access": request.user.access_control,
        "interview_id": interview_id
    }

    return render(request,"interview_status.html",context=context)


#for candidate deleteion
@login_required
def delete_candidate(request,interview_id,candidate_id):
    interview = Interview.objects.get(id=interview_id)
    candidate = Candidate.objects.get(id=candidate_id)
    if candidate.created_by==request.user.username:
        interview.candidates.remove(candidate)
        interview.save()
        candidate.delete()
        messages.success(request, "Deleted candidate")
        logger.info("Deleted candidate")
    else:
        messages.info(request, "Cannot Delete candidate")
    return redirect("interview_page",interview_id)