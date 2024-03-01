from django.urls import path

from .views import *

app_name = 'gudang'

urlpatterns = [
    path('all', GudangViewSet.as_view({
        'get': 'listGudang',
    })),
    path('create', GudangViewSet.as_view({
        'post': 'createGudang'
    })),
]