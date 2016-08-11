from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
import datetime

class Owner(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200, blank=True)
    
    def get_absolute_url(self):
        return '/app/owners/{}/'.format(self.id)
    
    def __str__(self):
        return self.name

class RiskType(models.Model):
    name = models.CharField(max_length=200)
    
    def get_absolute_url(self):
        return '/app/risk-types/{}/'.format(self.id)
    
    def __str__(self):
        return self.name
        
    def count_required_attributes_for_models(self):
        return self.required.filter(obj_type='MODEL').count()
    
    def count_required_attributes_for_versions(self):
        return self.required.filter(obj_type='VERSION').count()
        
class Model(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='models')
    risk_type = models.ForeignKey(RiskType, on_delete=models.CASCADE, related_name='models')
    
    def get_absolute_url(self):
        return '/app/models/{}/'.format(self.id)
        
    def name(self):
        ma = self.attributes.get(attribute__name='Название')
        rec = ma.current_record()
        if rec:
            return rec.string_value
        else:
            return "NA"
            
    def __str__(self):
        return self.name()
        
    def save(self):
        super(Model, self).save()
        risk_type = self.risk_type
        for req in risk_type.required.all():
            if req.obj_type == AttributeRequired.MOD:
                model_attribute = ModelAttribute()
                model_attribute.model = self
                model_attribute.attribute = req.attribute
                model_attribute.save()

class Version(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='versions')
    number = models.DecimalField(max_digits=5, decimal_places=2)
    
    def get_absolute_url(self):
        return '/app/model-versions/{}/'.format(self.id)
    
    class Meta:
        ordering = ['-number']
        
    def is_most_recent(self):
        if self.number == max([v.number for v in self.model.versions.all()]):
            return True
        return False
        
    def save(self):
        super(Version, self).save()
        risk_type = self.model.risk_type
        for req in risk_type.required.all():
            if req.obj_type == AttributeRequired.VER:
                version_attribute = VersionAttribute()
                version_attribute.version = self
                version_attribute.attribute = req.attribute
                version_attribute.save()
    
class Attribute(models.Model):
    string_type = 'STR'
    text_type = 'TEXT'
    date_type = 'DATE'
    markdown_type = 'MD'
    number_type = 'NUM'
    file_type = 'FILE'
    multiple_choice_type = 'MULT_CHOICE'
    
    TYPE_CHOICES = (
        (string_type, 'Short String'),
        (number_type, 'Numeric'),
        (date_type, 'Date'),
        (text_type, 'Long Text'),
        (markdown_type, 'Markdown Text'),
        (file_type, 'File'),
        (multiple_choice_type, 'Multiple Choice'),
    )
    
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    data_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=text_type)
    sort_order = models.IntegerField(default=-1)
    allow_multiple = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['sort_order']
    
    def get_absolute_url(self):
        return '/app/attributes/{}/'.format(self.id)
    
    def __str__(self):
        return self.name


class AttributeChoice(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='choices')
    name = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name


class AttributeRequired(models.Model):
    MOD = 'MODEL'
    VER = 'VERSION'
    OBJ_TYPES = (
        (MOD, MOD),
        (VER, VER)
    )
    risk_type = models.ForeignKey(RiskType, on_delete=models.CASCADE, related_name='required')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='required')
    obj_type = models.CharField(max_length=300, choices=OBJ_TYPES)
    
    class Meta:
        ordering = ['attribute__sort_order']
    
        
class ModelAttribute(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    valid_record_id = models.IntegerField(default=0)
    
    def current_record(self):
        if self.valid_record_id == 0:
            return None
        return self.records.get(record_id=self.valid_record_id)
        
    class Meta:
        ordering = ['attribute__sort_order']
        
    def __str__(self):
        return '{}: {}'.format(self.model, self.attribute.name)
    
class VersionAttribute(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    valid_record_id = models.IntegerField(default=0)
    
    def current_record(self):
        if self.valid_record_id == 0:
            return None
        return self.records.get(record_id=self.valid_record_id)
        
    class Meta:
        ordering = ['attribute__sort_order']
        
    def __str__(self):
        return '{} v{}: {}'.format(self.version.model, self.version.number, self.attribute.name)
    
class ModelAttributeRecord(models.Model):
    
    change_create = 'CREATE'
    change_update = 'UPDATE'
    change_delete = 'DELETE'
    
    CHANGE_CHOICES = (
        (change_create, 'Create'),
        (change_update, 'Update'),
        (change_delete, 'Delete'),
    )
    
    def upload_path(instance, filename):
        path = 'models/{}/{}/{}/{}'.format(instance.model_attribute.model.id, instance.model_attribute.attribute.id, instance.record_id, filename)
        print('path')
        print(path)
        return path
    
    model_attribute = models.ForeignKey(ModelAttribute, on_delete=models.CASCADE, related_name='records')
    
    record_id = models.IntegerField()                                       # record version number
    user = models.ForeignKey(User)                                          # who edited
    timestamp = models.DateTimeField(auto_now_add=True)                     # when record was created
    change_type = models.CharField(max_length=50, choices=CHANGE_CHOICES)   # type of change
    is_deleted = models.BooleanField(default=False)                         # indicates whether record was deleted
    
    string_value = models.CharField(max_length=500, blank=True)
    text_value = models.TextField(blank=True)
    
    markdown_value = models.TextField(blank=True)
    markdown_value_html = models.TextField(default='', editable = False, blank=True)
    
    date_value = models.DateField(null=True, blank=True)
    number_value = models.DecimalField(max_digits=24, decimal_places=6, null=True, blank=True)
    file_value = models.FileField(upload_to=upload_path, blank=True)
    
    class Meta:
        ordering = ['-record_id']
    
    def __str__(self):
        if self.model_attribute.attribute.data_type == Attribute.string_type:
            return str(self.string_value)
        if self.model_attribute.attribute.data_type == Attribute.text_type:
            return str(self.text_value)
        if self.model_attribute.attribute.data_type == Attribute.markdown_type:
            return str(self.markdown_value_html)
        if self.model_attribute.attribute.data_type == Attribute.date_type:
            return str(self.date_value)
        if self.model_attribute.attribute.data_type == Attribute.number_type:
            return str(self.number_value)
        if self.model_attribute.attribute.data_type == Attribute.file_type:
            return str(self.file_value)
        if self.model_attribute.attribute.data_type == Attribute.multiple_choice_type:
            set = [c.attribute_choice.name for c in self.choices.all()]
            return ', '.join(set)
        else:
            super(ModelAttributeRecord, self).str()
    
    def save(self):
        if ModelAttributeRecord.objects.filter(model_attribute=self.model_attribute):
            self.record_id = self.model_attribute.valid_record_id + 1
            self.change_type = ModelAttributeRecord.change_update
        else:
            self.record_id = 1
            self.change_type = ModelAttributeRecord.change_create
        self.model_attribute.valid_record_id = self.record_id
        self.model_attribute.save()
        if self.markdown_value:
            self.markdown_value_html = markdown(self.markdown_value)
        print(self.file_value)
        super(ModelAttributeRecord, self).save()
        
class ModelAttributeRecordChoice(models.Model):
    model_attribute_record = models.ForeignKey(ModelAttributeRecord, on_delete=models.CASCADE, related_name='choices')
    attribute_choice = models.ForeignKey(AttributeChoice, on_delete=models.CASCADE)
        
class VersionAttributeRecord(models.Model):
    
    change_create = 'CREATE'
    change_update = 'UPDATE'
    change_delete = 'DELETE'
    
    CHANGE_CHOICES = (
        (change_create, 'Create'),
        (change_update, 'Update'),
        (change_delete, 'Delete'),
    )
    
    def upload_path(instance, filename):
        return 'files/versions/{}/{}/{}/{}'.format(instance.version_attribute.version.id, instance.version_attribute.attribute.id, instance.record_id, filename)
    
    version_attribute = models.ForeignKey(VersionAttribute, on_delete=models.CASCADE, related_name='records')
    
    record_id = models.IntegerField()                                       # record version number
    user = models.ForeignKey(User)                                          # who edited
    timestamp = models.DateTimeField(auto_now_add=True)                     # when record was created
    change_type = models.CharField(max_length=50, choices=CHANGE_CHOICES)   # type of change
    is_deleted = models.BooleanField(default=False)                         # indicates whether record was deleted
    
    string_value = models.CharField(max_length=500, blank=True)
    text_value = models.TextField(blank=True)
    
    markdown_value = models.TextField(blank=True)
    markdown_value_html = models.TextField(default='', editable = False, blank=True)
    
    date_value = models.DateField(null=True)
    number_value = models.DecimalField(max_digits=24, decimal_places=6, null=True)
    file_value = models.FileField(upload_to=upload_path, blank=True)
    
    class Meta:
        ordering = ['-record_id']
    
    def __str__(self):
        if self.version_attribute.attribute.data_type == Attribute.string_type:
            return str(self.string_value)
        if self.version_attribute.attribute.data_type == Attribute.text_type:
            return str(self.text_value)
        if self.version_attribute.attribute.data_type == Attribute.markdown_type:
            return str(self.markdown_value_html)
        if self.version_attribute.attribute.data_type == Attribute.date_type:
            return str(self.date_value)
        if self.version_attribute.attribute.data_type == Attribute.number_type:
            return str(self.number_value)
        if self.version_attribute.attribute.data_type == Attribute.file_type:
            return str(self.file_value)
        if self.version_attribute.attribute.data_type == Attribute.multiple_choice_type:
            set = [c.attribute_choice.name for c in self.choices.all()]
            return ', '.join(set)
        else:
            super(VersionAttributeRecord, self).str()
    
    def save(self):
        if VersionAttributeRecord.objects.filter(version_attribute=self.version_attribute):
            self.record_id = self.version_attribute.valid_record_id + 1
            self.change_type = VersionAttributeRecord.change_update
        else:
            self.record_id = 1
            self.change_type = VersionAttributeRecord.change_create
        self.version_attribute.valid_record_id = self.record_id
        self.version_attribute.save()
        if self.markdown_value:
            self.markdown_value_html = markdown(self.markdown_value)
        super(VersionAttributeRecord, self).save()
        
class VersionAttributeRecordChoice(models.Model):
    version_attribute_record = models.ForeignKey(VersionAttributeRecord, on_delete=models.CASCADE, related_name='choices')
    attribute_choice = models.ForeignKey(AttributeChoice, on_delete=models.CASCADE)