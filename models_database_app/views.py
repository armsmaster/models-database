import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.decorators import login_required

from . import models
from . import forms

@login_required    
def index(request):
    template = loader.get_template('models_database_app/index.html')
    context = {
    }
    return HttpResponseRedirect('/app/risk-types/')
        
# RISK TYPE

class RiskTypeList(ListView):
    model = models.RiskType
    context_object_name = 'risk_types'
    template_name = 'models_database_app/risk_type_list.html'
        
class RiskTypeView(DetailView):
    template_name = 'models_database_app/risk_type_details.html'
    model = models.RiskType
    context_object_name = 'risk_type'

class RiskTypeCreate(CreateView):
    model = models.RiskType
    fields = ['name']
    template_name = 'models_database_app/risk_type_new.html'

class RiskTypeUpdate(UpdateView):
    model = models.RiskType
    fields = ['name']
    template_name = 'models_database_app/risk_type_edit.html'
    
# OWNER

class OwnerList(ListView):
    model = models.Owner
    context_object_name = 'owners'
    template_name = 'models_database_app/owner_list.html'


class OwnerView(DetailView):
    template_name = 'models_database_app/owner_details.html'
    model = models.Owner
    context_object_name = 'owner'
    

class OwnerCreate(CreateView):
    model = models.Owner
    fields = ['name', 'department']
    template_name = 'models_database_app/owner_new.html'


class OwnerUpdate(UpdateView):
    model = models.Owner
    fields = ['name', 'department']
    template_name = 'models_database_app/owner_edit.html'

# ATTRIBUTE
    
class AttributeList(ListView):
    model = models.Attribute
    context_object_name = 'attributes'
    template_name = 'models_database_app/attribute_list.html'
    
class AttributeView(DetailView, FormView):
    template_name = 'models_database_app/attribute_details.html'
    model = models.Attribute
    context_object_name = 'attribute'
    form_class = forms.AttributeChoice
    
    def get_success_url(self):
        object = self.get_object()
        return '/app/attributes/{}/'.format(object.id)
    
    def form_valid(self, form):
        choice = form.save(commit=False)
        choice.attribute = self.get_object()
        choice.save()
        return super(AttributeView, self).form_valid(form)
    
    
class AttributeCreate(CreateView):
    model = models.Attribute
    fields = ['name', 'data_type', 'description', 'sort_order', 'allow_multiple']
    template_name = 'models_database_app/attribute_new.html'

class AttributeUpdate(UpdateView):
    model = models.Attribute
    fields = ['name', 'description', 'sort_order', 'allow_multiple']
    template_name = 'models_database_app/attribute_edit.html'
    
# MODEL

class ModelList(ListView):
    model = models.Model
    context_object_name = 'models'
    template_name = 'models_database_app/model_list.html'


class ModelView(DetailView):
    template_name = 'models_database_app/model_details.html'
    model = models.Model
    context_object_name = 'model'
    

class ModelCreate(CreateView):
    model = models.Model
    form_class = forms.Model
    template_name = 'models_database_app/model_new.html'
    success_url = '/app/models/'
    
    def form_valid(self, form):
        self.object = form.save()
        name_attrib = models.Attribute.objects.get(name='Название')
        link = models.ModelAttribute(model=self.object, attribute=name_attrib)
        link.save()
        rec = models.ModelAttributeRecord(model_attribute=link, string_value=form.cleaned_data['model_name'], user=self.request.user)
        rec.save()
        return HttpResponseRedirect(self.get_success_url())
        

class ModelUpdate(UpdateView):
    model = models.Model
    fields = [ 'risk_type', 'owner']
    template_name = 'models_database_app/model_edit.html'
    context_object_name = 'model'
    

class ModelAttributeCreate(CreateView):
    model = models.ModelAttribute
    form_class = forms.ModelAttribute
    template_name = 'models_database_app/model_attribute_new.html'
    context_object_name = 'model_attribute'
    
    def get_context_data(self, **kwargs):
        context = super(ModelAttributeCreate, self).get_context_data(**kwargs)
        context['model_instance'] = models.Model.objects.get(pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.model = models.Model.objects.get(pk=self.kwargs['pk'])
        if self.object.attribute.allow_multiple:
            self.object.save()
        else:
            if not self.object.model.attributes.filter(attribute=self.object.attribute):
                self.object.save()
        return HttpResponseRedirect('/app/models/{}/'.format(self.object.model.id))
        
def ModelAttributeRecordCreate(request, model_attribute_id):
    object = models.ModelAttribute.objects.get(pk=model_attribute_id)
    if request.method == "POST":
        if object.attribute.data_type == models.Attribute.string_type:
            form = forms.ModelAttributeRecordString(request.POST)
        elif object.attribute.data_type == models.Attribute.text_type:
            form = forms.ModelAttributeRecordText(request.POST)
        elif object.attribute.data_type == models.Attribute.date_type:
            form = forms.ModelAttributeRecordDate(request.POST)
        elif object.attribute.data_type == models.Attribute.markdown_type:
            form = forms.ModelAttributeRecordMarkdown(request.POST)
        elif object.attribute.data_type == models.Attribute.number_type:
            form = forms.ModelAttributeRecordNumber(request.POST)
        elif object.attribute.data_type == models.Attribute.file_type:
            form = forms.ModelAttributeRecordFile(request.POST, request.FILES)
        elif object.attribute.data_type == models.Attribute.multiple_choice_type:
            form = forms.ModelAttributeRecordMultipleChoice(request.POST)
            choice_set = [(item.id, item.name) for item in object.attribute.choices.all()]
            form.fields['choices'].choices = choice_set
            if form.is_valid():
                rec = models.ModelAttributeRecord()
                rec.model_attribute = object
                rec.user = request.user
                rec.save()
                print(form.cleaned_data['choices'])
                for choice in form.cleaned_data['choices']:
                    c = models.AttributeChoice.objects.get(pk=int(choice))
                    x = models.ModelAttributeRecordChoice()
                    x.model_attribute_record = rec
                    x.attribute_choice = c
                    x.save()
            else:
                print(form.errors)
            return HttpResponseRedirect('/app/models/{}/'.format(object.model.id))
        rec = form.save(commit=False)
        rec.model_attribute = object
        rec.user = request.user
        rec.save()
        return HttpResponseRedirect('/app/models/{}/'.format(object.model.id))
    if object.attribute.data_type == models.Attribute.string_type:
        form = forms.ModelAttributeRecordString()
    elif object.attribute.data_type == models.Attribute.text_type:
        form = forms.ModelAttributeRecordText()
    elif object.attribute.data_type == models.Attribute.date_type:
        form = forms.ModelAttributeRecordDate()
    elif object.attribute.data_type == models.Attribute.markdown_type:
        form = forms.ModelAttributeRecordMarkdown()
    elif object.attribute.data_type == models.Attribute.number_type:
        form = forms.ModelAttributeRecordNumber()
    elif object.attribute.data_type == models.Attribute.file_type:
        form = forms.ModelAttributeRecordFile()
    elif object.attribute.data_type == models.Attribute.multiple_choice_type:
        form = forms.ModelAttributeRecordMultipleChoice(request.POST)
        choice_set = [(item.id, item.name) for item in object.attribute.choices.all()]
        form.fields['choices'].choices = choice_set
        form.fields['choices'].widget.attrs['size'] = str(len(choice_set))
    context = {
        'model_attribute': object, 
        'form': form,
    }
    template = loader.get_template('models_database_app/model_attribute_record_update.html')
    return HttpResponse(template.render(context, request))


class ModelAttributeView(DetailView):
    template_name = 'models_database_app/model_attribute_details.html'
    model = models.ModelAttribute
    context_object_name = 'model_attribute'
    
# VERSION

class VersionCreate(CreateView):
    model = models.Version
    form_class = forms.Version
    template_name = 'models_database_app/version_new.html'
    context_object_name = 'version'
    
    def get_context_data(self, **kwargs):
        context = super(VersionCreate, self).get_context_data(**kwargs)
        context['model_instance'] = models.Model.objects.get(pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.model = models.Model.objects.get(pk=self.kwargs['pk'])
        self.object.save()
        return HttpResponseRedirect('/app/models/{}/'.format(self.object.model.id))
        

class VersionView(DetailView):
    template_name = 'models_database_app/version_details.html'
    model = models.Version
    context_object_name = 'version'
    

class VersionAttributeCreate(CreateView):
    model = models.VersionAttribute
    form_class = forms.VersionAttribute
    template_name = 'models_database_app/version_attribute_new.html'
    context_object_name = 'version_attribute'
    
    def get_context_data(self, **kwargs):
        context = super(VersionAttributeCreate, self).get_context_data(**kwargs)
        context['version_instance'] = models.Version.objects.get(pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.version = models.Version.objects.get(pk=self.kwargs['pk'])
        if self.object.attribute.allow_multiple:
            self.object.save()
        else:
            if not self.object.version.attributes.filter(attribute=self.object.attribute):
                self.object.save()
        return HttpResponseRedirect('/app/model-versions/{}/'.format(self.object.version.id))
        

def VersionAttributeRecordCreate(request, version_attribute_id):
    object = models.VersionAttribute.objects.get(pk=version_attribute_id)
    if request.method == "POST":
        if object.attribute.data_type == models.Attribute.string_type:
            form = forms.VersionAttributeRecordString(request.POST)
        elif object.attribute.data_type == models.Attribute.text_type:
            form = forms.VersionAttributeRecordText(request.POST)
        elif object.attribute.data_type == models.Attribute.date_type:
            form = forms.VersionAttributeRecordDate(request.POST)
        elif object.attribute.data_type == models.Attribute.markdown_type:
            form = forms.VersionAttributeRecordMarkdown(request.POST)
        elif object.attribute.data_type == models.Attribute.number_type:
            form = forms.VersionAttributeRecordNumber(request.POST)
        elif object.attribute.data_type == models.Attribute.file_type:
            form = forms.VersionAttributeRecordFile(request.POST, request.FILES)
        elif object.attribute.data_type == models.Attribute.multiple_choice_type:
            form = forms.VersionAttributeRecordMultipleChoice(request.POST)
            choice_set = [(item.id, item.name) for item in object.attribute.choices.all()]
            form.fields['choices'].choices = choice_set
            if form.is_valid():
                rec = models.VersionAttributeRecord()
                rec.version_attribute = object
                rec.user = request.user
                rec.save()
                print(form.cleaned_data['choices'])
                for choice in form.cleaned_data['choices']:
                    c = models.AttributeChoice.objects.get(pk=int(choice))
                    x = models.VersionAttributeRecordChoice()
                    x.version_attribute_record = rec
                    x.attribute_choice = c
                    x.save()
            else:
                print(form.errors)
            return HttpResponseRedirect('/app/model-versions/{}/'.format(object.version.id))
        rec = form.save(commit=False)
        rec.version_attribute = object
        rec.user = request.user
        rec.save()
        return HttpResponseRedirect('/app/model-versions/{}/'.format(object.version.id))
    if object.attribute.data_type == models.Attribute.string_type:
        form = forms.VersionAttributeRecordString()
    elif object.attribute.data_type == models.Attribute.text_type:
        form = forms.VersionAttributeRecordText()
    elif object.attribute.data_type == models.Attribute.date_type:
        form = forms.VersionAttributeRecordDate()
    elif object.attribute.data_type == models.Attribute.markdown_type:
        form = forms.VersionAttributeRecordMarkdown()
    elif object.attribute.data_type == models.Attribute.number_type:
        form = forms.VersionAttributeRecordNumber()
    elif object.attribute.data_type == models.Attribute.file_type:
        form = forms.VersionAttributeRecordFile()
    elif object.attribute.data_type == models.Attribute.multiple_choice_type:
        form = forms.VersionAttributeRecordMultipleChoice(request.POST)
        choice_set = [(item.id, item.name) for item in object.attribute.choices.all()]
        form.fields['choices'].choices = choice_set
        form.fields['choices'].widget.attrs['size'] = str(len(choice_set))
    context = {
        'version_attribute': object, 
        'form': form,
    }
    template = loader.get_template('models_database_app/version_attribute_record_update.html')
    return HttpResponse(template.render(context, request))
    

class VersionAttributeView(DetailView):
    template_name = 'models_database_app/version_attribute_details.html'
    model = models.VersionAttribute
    context_object_name = 'version_attribute'

    
class VersionUpdate(UpdateView):
    model = models.Version
    fields = ['number']
    template_name = 'models_database_app/version_edit.html'
    context_object_name = 'version'