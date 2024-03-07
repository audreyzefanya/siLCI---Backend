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
    path('<str:gudang_id>', BarangGudangViewSet.as_view({
        'post': 'addBarangToGudang'
    })),
    path('barang-gudang/<uuid:gudang_id>/', BarangGudangViewSet.as_view({
        'get': 'listBarangPadaGudang',
    }), name='barang-gudang-list'),
    path('barang-gudang/detail/<uuid:gudang_id>/', BarangGudangViewSet.as_view({
        'get': 'detailGudang'
    }), name='detail-gudang'),
]