from django.shortcuts import render, redirect
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.
import datetime

def home(request):
    if request.method == 'GET':
        return render(request,'tool/home.html')

    if request.method == 'POST':
        name = request.POST.get('projname')
        new_proj = models.Project.objects.create(name=name)
        new_proj.save()
        return redirect(f'../../projectmanagementtool/proj?id={new_proj.id}')

def createNewProject(request):
    
    if request.method == 'GET':

        pendings = models.Project.get_pending()

        pid = request.GET.get('id')        
        proj = models.Project.get_by_id(int(pid))

        notes = models.Notes.get_by_proj_id(proj.id)
        bugs = models.Bugs.get_by_proj_id(proj.id)
        err = models.Errors.get_by_proj_id(proj.id)

        return render(request,'tool/proj_opened.html' , {'proj': proj, "notes":notes, "bugs":bugs, "errs":err ,"pendings":pendings})
        
    
@csrf_exempt
def AddNotes(request):
    typ = request.POST.get('type')
    data = request.POST.get('value')
    pid = request.POST.get('proj_id')
    
    project = models.Project.get_by_id(int(pid))

    if( typ == 'note'):
        new = models.Notes.objects.create(text = data, project= project)
        new.save()
    
    if(typ == 'bug'):
        new = models.Bugs.objects.create(text = data , project= project)
        new.save()
    
    if(typ == 'err'):
        new = models.Errors.objects.create(text = data, project= project )
        new.save()

    if(typ=='update'):
        field = request.POST.get('field')
        if field == 'note':
            new = models.Notes.get_by_id(int(pid))

        if field == 'bug':
            new = models.Bugs.get_by_id(int(pid))

        if field == 'err':
            new = models.Errors.get_by_id(int(pid))
        
        new.completed = True
        new.save()

        return JsonResponse({"id":new.id,"type":field})
    return JsonResponse({"id":new.id})
        

    


def showPending(request):
    if request.method == 'GET':
        p = models.Project.get_pending()
        return render(request, 'tool/pending.html', {'projects':p})
    


def showCompleted(request):
    if request.method == 'GET':
        p = models.Project.get_completed()
        return render(request, 'tool/completed.html', {'projects':p})
    


def markComplete(request):
    if request.method == 'GET':
        pid = request.GET.get('id')
        proj = models.Project.get_by_id(int(pid))
        proj.completed = True
        proj.completion_date = datetime.datetime.now()
        proj.save()
        return redirect(request.META["HTTP_REFERER"])
    

def delete(request):
    pass