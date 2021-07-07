from django.conf.urls import url
from core import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name="core/robots.txt", content_type='text/plain')),
    url(r'^$', views.index, name='index'),
    url(r'^reservation', views.reserve, name='reservation'),
    url(r'^info', views.info, name='info')
]
