from django.contrib import admin
from django.conf.urls import include, url
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView

from .schema import schema

urlpatterns = [
    url(r'^admin', include(admin.site.urls)),
    url(r'^graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    url(r'^api', GraphQLView.as_view(graphiql=False, schema=schema)),
    url(r'', TemplateView.as_view(template_name='index.html')),
]
