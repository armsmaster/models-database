from django import forms
from django.forms import widgets

from . import models

class Owner(forms.ModelForm):
    class Meta:
        model = models.Owner
        fields = ('name', 'department',)
        
class Attribute(forms.ModelForm):
    class Meta:
        model = models.Attribute
        fields = ('name', 'data_type', 'description', 'sort_order')
        
class AttributeChoice(forms.ModelForm):
    class Meta:
        model = models.AttributeChoice
        fields = ('name',)
        
class Model(forms.ModelForm):
    model_name = forms.CharField(max_length=200)
    
    class Meta:
        model = models.Model
        fields = ('risk_type', 'owner',)
        
class ModelEditOwner(forms.ModelForm):
    
    class Meta:
        model = models.Model
        fields = ('owner',)
        
class ModelAttribute(forms.ModelForm):
    class Meta:
        model = models.ModelAttribute
        fields = ('attribute',)
        
class ModelAttributeRecordString(forms.ModelForm):
    class Meta:
        model = models.ModelAttributeRecord
        fields = ('string_value',)
        
class ModelAttributeRecordText(forms.ModelForm):
    class Meta:
        model = models.ModelAttributeRecord
        fields = ('text_value',)
        
class ModelAttributeRecordMarkdown(forms.ModelForm):
    class Meta:
        model = models.ModelAttributeRecord
        fields = ('markdown_value',)
        
class ModelAttributeRecordDate(forms.ModelForm):
    class Meta:
        model = models.ModelAttributeRecord
        fields = ('date_value',)
        
class ModelAttributeRecordNumber(forms.ModelForm):
    class Meta:
        model = models.ModelAttributeRecord
        fields = ('number_value',)
        
class ModelAttributeRecordFile(forms.ModelForm):
    class Meta:
        model = models.ModelAttributeRecord
        fields = ('file_value',)
        
class ModelAttributeRecordMultipleChoice(forms.Form):
    choices = forms.MultipleChoiceField(choices=[], required=None, widget=forms.SelectMultiple(attrs={'size': '4'}))

class VersionAttributeRecordMultipleChoice(forms.Form):
    choices = forms.MultipleChoiceField(choices=[], required=None, widget=forms.SelectMultiple(attrs={'size': '4'}))
        
class Version(forms.ModelForm):
    class Meta:
        model = models.Version
        fields = ('number',)
        
class VersionAttribute(forms.ModelForm):
    class Meta:
        model = models.VersionAttribute
        fields = ('attribute',)
        
class VersionAttributeRecordString(forms.ModelForm):
    class Meta:
        model = models.VersionAttributeRecord
        fields = ('string_value',)
        
class VersionAttributeRecordText(forms.ModelForm):
    class Meta:
        model = models.VersionAttributeRecord
        fields = ('text_value',)
        
class VersionAttributeRecordMarkdown(forms.ModelForm):
    class Meta:
        model = models.VersionAttributeRecord
        fields = ('markdown_value',)
        
class VersionAttributeRecordDate(forms.ModelForm):
    class Meta:
        model = models.VersionAttributeRecord
        fields = ('date_value',)
        
class VersionAttributeRecordNumber(forms.ModelForm):
    class Meta:
        model = models.VersionAttributeRecord
        fields = ('number_value',)
        
class VersionAttributeRecordFile(forms.ModelForm):
    class Meta:
        model = models.VersionAttributeRecord
        fields = ('file_value',)

class AttributeRequired(forms.ModelForm):
    class Meta:
        model = models.AttributeRequired
        fields = ('attribute', 'obj_type',)