from django.contrib import admin
from django.urls import include, path
from graphene_django.views import GraphQLView

from .schema import schema

urlpatterns = [
    path('', include('sweeper.urls')),
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
]
