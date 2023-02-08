from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects


# Create your views here.
def projects(request):
    search_query, projects = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 6)

    context = { 'projects' : projects, 'search': search_query, 'custom_range':custom_range }
    return render(request,'projects/projects.html', context)
 
def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = Tag.objects.all()
    form = ReviewForm()

    if request.method == 'POST':
        try:
            form = ReviewForm(request.POST)
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()
            messages.success(request, 'You review was sucessfully submeitted.')
            projectObj.getVotedCount
            return redirect('project', pk=projectObj.id)
        except:
            messages.error(request, 'Sorry, you can only vote one time per project.')

    context = {'project': projectObj, 'tags': tags, 'form':form }
    return render(request,'projects/single-project.html',context) 

'''
           - -C-R-U-D- -
'''
@login_required(login_url="login")
def createProject(request):
    page = 'create'
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            messages.success(request, 'The project was successfully created.')
            return redirect('account')
        else:
            messages.error(request, 'Error occurred when the project was created.')
            return redirect('account')

    context = {'form': form, 'page':page}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def updateProject(request, pk):
    page = 'update'
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == "POST":
        # This will split the new tags where we have a , or " "
        newtags = request.POST.get('newtags').replace(',', " ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            messages.success(request, 'The project was successfully updated.')
            return redirect('account')
        else:
            messages.error(request, 'Error occurred when the project was updated.')
            return redirect('account')

    context ={'form': form, 'page':page, 'project': project}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == "POST":
        project.delete()
        messages.success(request, 'The project was successfully deleted.')
        return redirect('account')
    
    context = {'project': project}
    return render(request, 'delete_template.html', context)