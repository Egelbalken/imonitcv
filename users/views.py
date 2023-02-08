from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .utils import searchProfiles, paginateProfiles
# Adds a extra filterfunction to filter something and something more.
from .models import Profile, Message
from django.core.mail import send_mail

def loginUser(request):
    page = 'login'
    # if autenticated return to profles.
    if request.user.is_authenticated:
        return redirect("profiles")

    # Ceck for the credentials.
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            print("Username does not exist")
            messages.error(request, 'Username does not exist.')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #messages.success(request, 'User successfully loged in.')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            print("username or password is incorrect",user)
            messages.error(request, 'username or password is incorrect.')

    context= {'page':page}
    return render(request, 'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User successfully loged out.')
    return redirect('login')

def registerUser(request):
    page= 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created.')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error occurred during registraion creation.')

    context={'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)

# Create your views here.
def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 3)

    context = {'profiles': profiles, 'search': search_query, 'custom_range':custom_range}
    return render(request, 'users/profiles.html' , context)

'''
'''
def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile':profile, 'topSkills': topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects':projects}
    return render(request, 'users/account.html', context)

@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    #fill the form with an instance of a profile.
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account was successfully updated.')
            return redirect('account')
        else:
            messages.error(request, 'Error occurred when the account was created.')
            return redirect('account')
    context = {'form':form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url="login")
def createSkill(request):
    page = 'create'
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill successfully created.')
            return redirect('account')
        else:
            messages.error(request, 'Error occurred when the skill was created.')
            return redirect('account')


    context={'form': form, 'page':page}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url="login")
def updateSkill(request, pk):
    page = 'edit'
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            messages.error(request, 'Error occurred when the skill was updated.')
            return redirect('account')


    context={'form': form, 'page':page}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was successfully deleted.')
        return redirect('account')

    context={'object': skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()

    context= {'messageRequests':messageRequests, 'unreadCount':unreadCount }
    return render(request, 'users/inbox.html', context)

@login_required(login_url="login")
def viewMessage(request,pk):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=True).count()
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context= {'message':message, 'unreadCount':unreadCount}
    return render(request, 'users/message.html', context)


def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == "POST":
        form = MessageForm(request.POST)
        
        #if valid
        if form.is_valid():
            message = form.save(commit=False)
            # do we have a sender?
            message.sender = sender
            # do we have a recipient
            message.recipient = recipient
            # if we hade them they are authenticated so assig them 
            if sender:
                message.name = sender.name
                message.email = sender.email
            
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            # send them back to the site
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient':recipient, 'form':form}
    return render(request, 'users/message_form.html', context)