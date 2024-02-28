from django.urls import path
from .views import * 

app_name = 'barang'

urlpatterns = [
    path('all', BarangViewSet.as_view({
        'get': 'getAllBarang',
    })),
    path('create', BarangViewSet.as_view({
        'post': 'createBarang'
    })),
    path('perusahaan/all', PerusahaanViewSet.as_view({
        'get': 'getAllPerusahaan'
    })),
    path('perusahaan/create', PerusahaanViewSet.as_view({
        'post': 'createPerusahaan'
    })),
    path('perusahaan/<str:perusahaan_id>', PerusahaanViewSet.as_view({
        'get': 'getBarangPerusahaan',
        'put': 'addBarangToPerusahaan'
    })),
]