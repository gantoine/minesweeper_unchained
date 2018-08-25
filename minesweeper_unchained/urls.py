from django.contrib import admin
from django.conf.urls import include, url
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import ensure_csrf_cookie

from .schema import schema

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^graphiql', GraphQLView.as_view(graphiql=True, schema=schema)),
    url(r'^graphql', GraphQLView.as_view(graphiql=False, schema=schema)),
    url(r'', ensure_csrf_cookie(TemplateView.as_view(template_name='index.html'))),
]
