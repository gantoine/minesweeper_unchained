from django.contrib import admin
from django.conf.urls import include, url
from graphene_django.views import GraphQLView

from .schema import schema

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    url(r'', include('sweeper.urls')),
]
