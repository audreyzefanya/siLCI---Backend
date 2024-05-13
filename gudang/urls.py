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
    })),
    path('barang-gudang/detail/<uuid:gudang_id>/', BarangGudangViewSet.as_view({
        'get': 'detailGudang'
    })),
    path('barang-gudang/update/stok', BarangGudangViewSet.as_view({
        'put': 'addStokGudang'
    })),
    path('barang-gudang/update/<uuid:gudang_id>/', BarangGudangViewSet.as_view({
        'put': 'updateDetailGudang'
    })),
    path('permintaanpengiriman/<str:gudang_id>', PermintaanPengirimanViewSet.as_view({
        'get': 'getDaftarPengirimanGudang',
        'post': 'addPermintaanPengiriman'
    })),
    path('statuspengiriman/<str:kode_permintaan>', PermintaanPengirimanViewSet.as_view({
        'put': 'updateStatusGudang',
    })),
    path('statuspengiriman/<str:kode_permintaan>', PermintaanPengirimanViewSet.as_view({
        'put': 'statusPengirimanGudang',
    })),
    path('barang-gudang/update/reduce-stok', BarangGudangViewSet.as_view({
        'put': 'reduceStokGudang'
    }), name='reduce_stok'),

]