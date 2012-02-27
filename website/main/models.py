import os, random
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
import settings
from pymodules.calculate_distance import calculate_distance
from pymodules.check_similar import check_similar

class Professor(models.Model):
    name = models.CharField(_("Name"), max_length=200, unique=True, help_text=_("Should be same as displayed on portal.acm.org"))
    image = models.ImageField(_("Image of Professer"), upload_to=os.path.join(settings.MEDIA_ROOT, 'img/faces'), default=os.path.join(settings.MEDIA_ROOT, 'img/faces/blank_face.jpg'))
    domain = models.CharField(_("Website"), max_length=100)
    university = models.CharField(_("University"), max_length=200)
    address = models.TextField(_("Address"))
    location = models.CharField(_("Location"), max_length=200,)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name        
    
    def get_image_url(self):
        return str('/media' + str(self.image)[len(settings.MEDIA_ROOT):])

    def is_in_confrence(self, confrence_id=1):
        cp_set = ConfrenceProfile().objects.all().filter(pk=conf_id)
        for c in cp_set:
            if c.professor.name == self.name:
                return True
        return False
    

class Confrence(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    year = models.IntegerField(_("Year"), max_length=4)
    description = models.TextField(_("Description"))

    def __unicode__(self):
        return self.name

class ConfrenceProfile(models.Model):
    professor = models.ForeignKey(Professor)
    confrence = models.ForeignKey(Confrence)
    co_authors = models.TextField(_("Co Authors"))
    cite_authors = models.TextField(_("Cite Authors"))
    ref_authors = models.TextField(_("Ref Authors"))
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True)
    
    class Meta:
        unique_together = (("professor", "confrence"),)
    def __unicode__(self):
        return self.professor.name

    def sort_others_by_distance(self, count):
        professors = Professor.objects.all()
        p_select = []
        
        if count==None or int(count)>len(professors):
            p_select = professors
        else:
            for i in range(int(count)):
                rand_p = professors[random.randrange(len(professors))]
                while rand_p in p_select:
                    rand_p = professors[random.randrange(len(professors))]
                p_select.append(rand_p)

        result = []
        for p in p_select:
            if p == self.professor:
                ##result.append({'distance':0, 'professor':self.professor})
                continue
            distance = calculate_distance(self.professor.location,p.location)
            result.append({'distance':distance, 'professor':p})
        sorted_result = sorted(result , key=lambda k: k['distance'])
        return sorted_result

    def get_co_papers(self):
        result = []
        prof_set = Professor.objects.all().order_by('name')

        for c in str(self.co_authors).split(';'):
            auth = []
            c_split = c.split('|')
            for p in prof_set:
                if self.professor.name.lower() == p.name.lower():
                    continue
                else:
                    try:
                        for c_sp in c_split[1].split(','):
                            if p.name.lower().strip() == str(c_sp).strip().lower():
                                auth.append(p)
                    except:
                        continue
            result.append({'title':c_split[0], 'authors':auth})
        return result

    def get_cited_papers(self):
        result = []
        prof_set = Professor.objects.all().order_by('name')

        for c in str(self.cite_authors).split(';'):
            auth = []
            c_split = c.split('|')
            for p in prof_set:
                if self.professor.name.lower() == p.name.lower():
                    continue
                else:
                    try:
                        for c_sp in c_split[1].split(','):
                            if p.name.lower().strip() == str(c_sp).strip().lower():
                                auth.append(p)
                    except:
                        continue
            result.append({'title':c_split[0], 'citers':auth})
        return result

    def get_referenced_papers(self):
        result = []
        prof_set = Professor.objects.all().order_by('name')

        for c in str(self.ref_authors).split(';'):
            auth = []
            c_split = c.split('|')
            for p in prof_set:
                if self.professor.name.lower() == p.name.lower():
                    continue
                else:
                    try:
                        for c_sp in c_split[1].split(','):
                            if p.name.lower().strip() == str(c_sp).strip().lower():
                                auth.append(p)
                    except:
                        continue
            result.append({'title':c_split[0], 'referers':auth})
        return result
