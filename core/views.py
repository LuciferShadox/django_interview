from django.shortcuts import render,redirect
from core.models import Interview,Candidate,UserInterview
from django.contrib.auth.decorators import login_required
from django.contrib import messages #import messages

from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def list_interviews(request):
    #check user_type 
    if request.user.is_staff:
        interviews = Interview.objects.all()
    else:
        interviews=None
        # if user in interview.users
        # check type of user
        #then show the interviews

    
    context={
        "interviews":interviews
    }
    return render(request,"interviews.html",context=context)

@login_required
def add_interview(request):
    if not request.user.is_staff:
        logger.info("User is not Staff")
        messages.warning(request,"Sorry do not have permission to add interviews")
        return redirect("interviews")
    logger.info("User is Staff")
    if request.method=='POST':
        logger.info("Request is Post")

        client_name = request.POST["client_name"]
        project_name = request.POST["project_name"]
        description = request.POST["description"]
        start_date = datetime.now()
        logger.info("Form Arguments are processed")
        name = request.user.name
        if name is None:
            name = request.user.username
        logger.info("Creating Interview object")
        interview = Interview(client_name=client_name,start_date=start_date,
                                 interviewer_name=name,
                                 name=project_name,description=description)
        
        interview.save()
        interview.accessible_users.add(request.user)
        interview.save()
        logger.info("Saving Interview object")
        logger.info("Creating User Interview object")
        user_interview = UserInterview(user=request.user,interview=interview)
        user_interview.save()
        logger.info("Saving UserInterview object")
        logger.info("Redirecting to Interview Page")
        return redirect("interviews")
        #create user interview object and add self as user 
        # accessible_users # later in configuration
        # very much later
        # if there are other users create objects of them too

    return render(request,"add_interview.html")



