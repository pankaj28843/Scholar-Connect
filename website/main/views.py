import random, string, hashlib,datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from main.models import *
from main.forms import *
from crawl_data import create_confrence_profile
from pymodules.google_dictionary_search import dictionary_search

p_id = Professor.objects.get(name='niloy ganguly').id

def check_status_profile(request):
    return 

def dictionary(request, query):
    response = dictionary_search(query)
    return HttpResponse("<pre>"+response+"</pre>")

def index(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = ProfessorSearchForm(request.POST)
        if form.is_valid():
            confrence = form.cleaned_data['confrence']
            professor = form.cleaned_data['professor']
            cp = get_object_or_404(ConfrenceProfile, confrence=confrence, professor=professor)
            return render_to_response("main/dashboard.html", {'cp':cp,}, context_instance=context)
        else:
            return render_to_response("main/index.html", {'form':form,}, context_instance=context)
    else:
        form = ProfessorSearchForm()
        return render_to_response("main/index.html", {'form':form,}, context_instance=context)
    
def add_new_prof(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response("main/add_new_prof_done.html", context_instance=context)
        else:
            return render_to_response("main/add_new_prof.html", {'form':form,}, context_instance=context)
    else:
        form = ProfessorForm(request.POST)
        return render_to_response("main/add_new_prof.html", {'form':form,}, context_instance=context)

def show_prof_details(request, prof_id):
    context = RequestContext(request)
    prof = get_object_or_404(Professor, pk=prof_id)
    return render_to_response("main/show_prof_details.html", {'prof':prof,} ,  context_instance=context)

def show_map(request, cp_id, count=None):
    context = RequestContext(request)
    cp = get_object_or_404(ConfrenceProfile, pk=cp_id)
    result = cp.sort_others_by_distance(count)
    #print result
    return render_to_response("main/map.html", {'result':result, 'prof':cp.professor, 'cp':cp}, context_instance=context)

def show_co_authors(request, cp_id):
    context = RequestContext(request)
    cp = get_object_or_404(ConfrenceProfile, pk=cp_id)
    confrence = cp.confrence
    paper_list = cp.get_co_papers()
    participants = []
    
    for p in Professor.objects.all():
        if p == cp.professor:
            continue
        count = 0
        for paper in paper_list:
            if p in paper['authors']:
                count = count+1
        print count
        
        if count:
            participants.append({'count':count, 'professor':p })
    participants = sorted(participants , key=lambda k: -k['count'])
    
    return render_to_response("main/co_authors.html", {'paper_list':paper_list, 'participants':participants, 'prof':cp.professor}, context_instance=context)

def show_cite_authors(request, cp_id):
    context = RequestContext(request)
    cp = get_object_or_404(ConfrenceProfile, pk=cp_id)
    confrence = cp.confrence
    paper_list = cp.get_cited_papers()
    participants = []
    
    for p in Professor.objects.all():
        if p == cp.professor:
            continue
        count = 0
        for paper in paper_list:
            if p in paper['citers']:
                count = count+1
        if count:
            participants.append({'count':count, 'professor':p })
    participants = sorted(participants , key=lambda k: -k['count'])
    
    return render_to_response("main/cite_authors.html", {'paper_list':paper_list, 'participants':participants, 'prof':cp.professor}, context_instance=context)

def show_ref_authors(request, cp_id):
    context = RequestContext(request)
    cp = get_object_or_404(ConfrenceProfile, pk=cp_id)
    confrence = cp.confrence
    paper_list = cp.get_referenced_papers()
    participants = []
    
    for p in Professor.objects.all():
        if p == cp.professor:
            continue
        count = 0
        for paper in paper_list:
            if p in paper['referers']:
                count = count+1
        if count:
            participants.append({'count':count, 'professor':p })
    participants = sorted(participants , key=lambda k: -k['count'])
    
    return render_to_response("main/ref_authors.html", {'paper_list':paper_list, 'participants':participants, 'prof':cp.professor}, context_instance=context)
