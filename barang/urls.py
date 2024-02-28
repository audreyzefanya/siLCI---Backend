from django.urls import path
from .views import * 

app_name = 'barang'

urlpatterns = [
    path('all', BarangViewSet.as_view({
        'get': 'getAllBarang',
    })),
    path('create', BarangViewSet.as_view({
        'post': 'createBarang'
    }))
]