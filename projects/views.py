from django.shortcuts import render
from .models import Project 

# Create your views here.

# Zeigt ALLE Projekte (öffentlich)
def project_list(request):    
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


# Zeigt EIN Projekt (Login required)
def project_detail(request, pk):    
    project = Project.objects.get(pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})