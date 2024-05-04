from django.urls import path

from .views import *

app_name = 'pabrik'

urlpatterns = [
    path('allpabrik', PabrikViewSet.as_view({
        'get': 'getAllPabrik',
    })),
    path('allbarangpabrik', PabrikViewSet.as_view({
        'get': 'getAllBarangPabrik',
    })),
    path('allbatchproduksi', BatchProduksiViewSet.as_view({
        'get': 'getAllBatchProduksiStatus',
    })),
    path('allpermintaanpengiriman', PermintaanPengirimanViewSet.as_view({
        'get': 'getAllPermintaanPengiriman',
    })),
    path('create', PabrikViewSet.as_view({
        'post': 'createPabrik'
    })),
    path('<str:pabrik_name>', PabrikViewSet.as_view({
        'get': 'getPabrik',
        'put': 'updatePabrik'
    })),
    path('batch/<str:pabrik_name>', BatchProduksiViewSet.as_view({
        'get': 'getAllBatchProduksiInPabrik',
        'post': 'addBatchProduksiToPabrik'
    })),
    path('batch/<str:pabrik_name>/<str:batch_code>', BatchProduksiViewSet.as_view({
        'get': 'getDetailBatchProduksiInPabrik',
        'put': 'updateBatchProduksiInPabrik'
    })),
    path('barang/<str:pabrik_name>', BarangPabrikViewSet.as_view({
        'get': 'getBarangInPabrik',
        'post': 'addBarangToPabrik'
    })),
    path('barang/<str:pabrik_name>/<str:barang_id>', BarangPabrikViewSet.as_view({
        'put': 'updateStokBarangInPabrik',
    })),
    path('permintaanpengiriman/<str:pabrik_name>', PermintaanPengirimanViewSet.as_view({
        'get': 'getDaftarPengiriman',
        'post': 'addPermintaanPengiriman'
    })),
    path('statuspengiriman/<str:kode_permintaan>', PermintaanPengirimanViewSet.as_view({
        'put': 'updateStatus',
    })),
    #     path('detail/<str:pabrik_id>', PabrikViewSet.as_view({
    #     'get': 'detailPabrik'
    # })),
    #     path('update/<str:pabrik_id>', PabrikViewSet.as_view({
    #     'put': 'updatePabrik'
    # })),
]