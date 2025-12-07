# projects/views.py ← DIE PERFEKTE ENDVERSION
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project


# 1. Öffentliche Projektliste – eingeloggte User sehen ALLES
def public_list(request):
    if request.user.is_authenticated:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(is_public_demo=True)
    
    # WICHTIG: .order_by() hier, nicht vorher!
    projects = projects.order_by('-created_date')
    
    return render(request, 'projects/public_list.html', {
        'projects': projects
    })

# 2. SECRET LAB – nur für eingeloggte User
@login_required(login_url='/accounts/login/')
def secret_lab(request):
    projects = Project.objects.all().order_by('-created_date')
    return render(request, 'projects/secret_lab.html', {
        'projects': projects,
        'user': request.user
    })


# 3. Detailansicht (optional – später)
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Nicht-öffentliche Projekte nur für eingeloggte User
    if not project.is_public_demo and not request.user.is_authenticated:
        return render(request, 'projects/login_required.html')
    return render(request, 'projects/project_detail.html', {'project': project})