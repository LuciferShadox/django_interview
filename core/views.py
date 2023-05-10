from django.shortcuts import render,redirect
from core.models import Interview,Candidate,User,UserInterview
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages #import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
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
        user_interview = UserInterview(user=request.user,interview=interview,access_control="CO")
        user_interview.save()
        logger.info("Saving UserInterview object")
        logger.info("Redirecting to Interview Page")
        return redirect("interviews")
        #create user interview object and add self as user 
        # accessible_users # later in configuration
        # very much later
        # if there are other users create objects of them too

    return render(request,"add_interview.html")



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
    user_interview = UserInterview.objects.get(user=request.user,interview=interview_id)
    context={
        "candidates":candidates,
        "access": user_interview.access_control,
        "interview_id": interview_id
    }

    return render(request,"interview_status.html",context=context)

def login_view(request):
    # use next keyword and goto the url
    if request.user.is_authenticated:
        return redirect("interviews")

    if request.method == 'POST':
        
        email_id = request.POST["email"]
        password = request.POST["password"]
        next_url = request.GET.get("next")
        user = authenticate(request,email=email_id,password=password)
        if user is not None:
            login(request,user)
            if next_url is None:
                return redirect("interviews")
            else:
                return redirect(next_url)
        else:
            messages.error(request,"Login Failed. Check Username and Password")
    
    return render(request,"login.html")

def register(request):
    # email_id 
    # username 
    # password
    if request.method == 'POST':
        username = request.POST['username']
        email_id = request.POST['email_id']
        password = request.POST['password']
        password_verify = request.POST['password_verify']
        if password==password_verify:
            #create model
            user = User.objects.create(username=username,email=email_id,password=make_password(password))
            user.save()
            return redirect("login")
    return render(request,"signup.html")

@login_required
def test_view(request):
    return render(request,"base.html")


def home(request):
    return redirect("")

