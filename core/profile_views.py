from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages #import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from core.models import User




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
    if request.user.is_staff:
        if request.method == 'POST':
            username = request.POST['username']
            email_id = request.POST['email_id']
            password = request.POST['password']
            password_verify = request.POST['password_verify']
            role = request.POST['role']
            if password==password_verify:
                #create model
                user = User.objects.create(username=username,email=email_id,
                                           password=make_password(password),access_control=role)
                user.save()
                if request.POST["next"]:
                    return redirect(request.POST["next"])
                return redirect("interviews")

    next_url = request.GET.get('next')
    redirect_field_name = "next"
    redirect_field_value = next_url
    context={
        "redirect_field_name":redirect_field_name,
        "redirect_field_value":redirect_field_value,
    }
    return render(request,"signup.html",context=context)


