from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
import django.contrib.auth.views
from django.contrib.auth.decorators import login_required, permission_required

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', django.contrib.auth.views.login, name='login'),
    url(r'^risk-types/$', login_required(views.RiskTypeList.as_view())),
    url(r'^risk-types/new/$', login_required(views.RiskTypeCreate.as_view())),
    url(r'^risk-types/edit/(?P<pk>[0-9]+)/$', login_required(views.RiskTypeUpdate.as_view())),
    url(r'^risk-types/(?P<pk>[0-9]+)/$', login_required(views.RiskTypeView.as_view())),
    url(r'^owners/$', login_required(views.OwnerList.as_view())),
    url(r'^owners/new/$', login_required(views.OwnerCreate.as_view())),
    url(r'^owners/edit/(?P<pk>[0-9]+)/$', login_required(views.OwnerUpdate.as_view())),
    url(r'^owners/(?P<pk>[0-9]+)/$', login_required(views.OwnerView.as_view())),
    url(r'^attributes/$', login_required(views.AttributeList.as_view())),
    url(r'^attributes/new/$', login_required(views.AttributeCreate.as_view())),
    url(r'^attributes/edit/(?P<pk>[0-9]+)/$', login_required(views.AttributeUpdate.as_view())),
    url(r'^attributes/(?P<pk>[0-9]+)/$', login_required(views.AttributeView.as_view())),
    url(r'^models/$', login_required(views.ModelList.as_view())),
    url(r'^models/new/$', login_required(views.ModelCreate.as_view())),
    url(r'^models/(?P<pk>[0-9]+)/$', login_required(views.ModelView.as_view())),
    url(r'^models/edit/(?P<pk>[0-9]+)/$', login_required(views.ModelUpdate.as_view())),
    url(r'^models/(?P<pk>[0-9]+)/new-attribute/$', login_required(views.ModelAttributeCreate.as_view())),
    url(r'^models/update-attribute/(?P<model_attribute_id>[0-9]+)/$', login_required(views.ModelAttributeRecordCreate)),
    url(r'^model-attribute/(?P<pk>[0-9]+)/$', login_required(views.ModelAttributeView.as_view())),
    url(r'^models/(?P<pk>[0-9]+)/new-version/$', login_required(views.VersionCreate.as_view())),
    url(r'^model-versions/(?P<pk>[0-9]+)/$', login_required(views.VersionView.as_view())),
    url(r'^model-versions/(?P<pk>[0-9]+)/new-attribute/$', login_required(views.VersionAttributeCreate.as_view())),
    url(r'^model-versions/update-attribute/(?P<version_attribute_id>[0-9]+)/$', login_required(views.VersionAttributeRecordCreate)),
    url(r'^version-attribute/(?P<pk>[0-9]+)/$', login_required(views.VersionAttributeView.as_view())),
    url(r'^model-versions/edit/(?P<pk>[0-9]+)/$', login_required(views.VersionUpdate.as_view())),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)