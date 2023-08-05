from django.conf.urls import url
from . import views, MAGIC_ID


_MODULE_MAGIC_ID_ = MAGIC_ID

urlpatterns = [
                       url(r'^login/$', views.login, name="sso_login"),
                       url(r'^reqeusttoken/$', views.api_requesttoken, name="sso_requesttoken"),
                       url(r'^authtoken/$', views.api_authtoken, name="sso_authtoken")
]
